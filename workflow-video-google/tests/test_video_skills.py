"""Behavior checks for local helpers; no network or paid model calls."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
import wave

SKILLS = Path(__file__).resolve().parents[1] / 'skills'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


project = module('video_project', SKILLS/'video-workflow/scripts/project.py')
animatic = module('video_animatic', SKILLS/'video-assemble/scripts/render_animatic.py')


def save(root, name, data):
    p = root/name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')


def ppm(path, color):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b'P6\n32 32\n255\n' + bytes(color)*32*32)


def wav(path, duration):
    with wave.open(str(path), 'wb') as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(16000)
        audio.writeframes(b''.join(struct.pack('<h', int(1200*math.sin(2*math.pi*220*i/16000))) for i in range(int(duration*16000))))


def fixture(root, long=False):
    fmt, platform = ('youtube-long', 'youtube') if long else ('short', 'youtube-shorts')
    env = {'schema_version':'1.0', 'project_id':'coffee', 'version':1}
    state = {**env, 'brief':{'format':fmt,'platform':platform,'target_duration_s':2,'aspect_ratio':'16:9' if long else '9:16','audio_mode':'none'},
             'budget':{'max_credits':None,'max_attempts_per_shot':2},'artifacts':[]}
    script = {**env,'format':fmt,'platform':platform,
              'hook':{'hook_id':'H01','beat_id':'B01','promise':'A pause in the morning','visual':'A cup on the desk','spoken':'','on_screen_text':'','payoff_beat_id':'B02'},
              'chapters':[{'chapter_id':'C01','title':'Morning','purpose':'A quiet moment'}] if long else [],
              'beats':[{'beat_id':bid,'role':role,'chapter_id':'C01' if long else None,'spoken':'','visual':'A cup moving','estimated_duration_s':1,'source_urls':[]}
                       for bid,role in [('B01','hook'),('B02','payoff')]]}
    if long:
        script['packaging']={'title_concept':'A quiet morning','thumbnail_concept':'The cup','promise':'See a pause'}
    shots, pairs = [], []
    for i in range(1,3):
        sid=f'S0{i}'
        shot={'shot_id':sid,'scene_id':'SC01','beat_ids':[f'B0{i}'],'purpose':'Tell the beat','duration_s':1,'generation_duration_s':4,
              'camera':'static close-up','start_state':'cup on table','end_state':'hand touches cup','motion':'hand approaches',
              'reference_ids':[],'audio_mode':'none','audio_cue_ids':[],
              'continuity':{'screen_direction':'left to right','eyeline':'cup','subject_positions':'center','props_state':'full cup','lighting':'morning'},
              'transition':{'type':'cut' if i==1 else 'end','target_shot_id':'S02' if i==1 else None},'handles':{'head_s':0,'tail_s':0}}
        shots.append(shot)
        pair={'shot_id':sid,'reference_ids':[],'review':{'status':'pass','notes':'Synthetic fixture'}}
        for end,color in [('start',(255,0,0)),('end',(0,0,255))]:
            rel=f"frames weird ' name/{sid}/{end}.ppm"
            ppm(root/rel,color)
            aid=f'frame.{sid}.{end}'
            pair[f'{end}_path']=rel
            pair[f'{end}_artifact_id']=aid
            pair[f'{end}_prompt']='Synthetic fixture'
            state['artifacts'].append({'id':aid,'kind':'image','scope':sid,'version':1,'path':rel,'status':'ready',
                                       'depends_on':[{'id':f'frame.{sid}.start','version':1}] if end=='end' else [],
                                       'review':{'status':'pass','notes':'Synthetic fixture'}})
        pairs.append(pair)
    save(root,'project.json',state)
    save(root,'script.json',script)
    save(root,'shotlist.json',{**env,'timing_basis':'action','shots':shots})
    save(root,'frames.json',{**env,'pairs':pairs})
    edit={**env,'mode':'animatic','width':320,'height':180,'fps':12,'audio_path':None,
          'segments':[{'shot_id':p['shot_id'],'start_frame':p['start_path'],'end_frame':p['end_path'],'duration_s':1} for p in pairs]}
    save(root,'edit-plan.json',edit)
    return state,script,edit


class ProjectChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.state,self.script,self.edit=fixture(self.root)
    def tearDown(self):
        self.tmp.cleanup()
    def errors(self):
        return project.validate(self.root)[0]
    def test_short_valid(self):
        self.assertEqual(self.errors(),[])
    def test_long_valid(self):
        fixture(self.root,long=True)
        self.assertEqual(self.errors(),[])
    def test_missing_payoff(self):
        self.script['hook']['payoff_beat_id']='B99'
        save(self.root,'script.json',self.script)
        self.assertTrue(any('payoff' in e for e in self.errors()))
    def test_missing_end_frame(self):
        (self.root/self.state['artifacts'][1]['path']).unlink()
        self.assertTrue(any('missing or empty' in e for e in self.errors()))
    def test_stale_ready_dependency(self):
        self.state['artifacts'][0]['version']=2
        save(self.root,'project.json',self.state)
        self.assertTrue(any('stale dependency' in e for e in self.errors()))
    def test_revision_targets_dependents_only_and_backup(self):
        affected=project.revise(self.root,'frame.S01.start','changed pose')
        self.assertEqual(affected,['frame.S01.end','frame.S01.start'])
        new=project.read_json(self.root/'project.json')
        self.assertEqual(new['artifacts'][0]['version'],2)
        self.assertEqual(new['artifacts'][2],self.state['artifacts'][2])
        self.assertEqual(new['artifacts'][1]['status'],'needs-revision')
        self.assertEqual(len(list((self.root/'.manifest-backups').glob('*.json'))),1)
    def test_dependency_cycle(self):
        self.state['artifacts'][0]['depends_on']=[{'id':'frame.S01.end','version':1}]
        save(self.root,'project.json',self.state)
        self.assertTrue(any('cycle' in e for e in self.errors()))
    def test_path_escape(self):
        self.state['artifacts'][0]['path']='../outside.ppm'
        save(self.root,'project.json',self.state)
        self.assertTrue(any('escapes project' in e for e in self.errors()))
    def test_invalid_selector(self):
        self.state['artifacts'].append({'id':'shot.S01','kind':'document','version':1,'path':'shotlist.json','selector':'/shots/99','status':'ready','depends_on':[],'review':{'status':'pass','notes':''}})
        save(self.root,'project.json',self.state)
        self.assertTrue(any('invalid selector' in e for e in self.errors()))
    def test_selected_running_take_rejected(self):
        env={'schema_version':'1.0','project_id':'coffee','version':1}
        save(self.root,'renders.json',{**env,'capability':{},'takes':[{'take_id':'T1','shot_id':'S01','status':'running','path':None,'input_versions':[{'id':'frame.S01.start','version':1}],'review':{'status':'pass','notes':''}}],'selected':{'S01':'T1'}})
        self.assertTrue(any('requires downloaded' in e for e in self.errors()))
    def test_audio_cue_out_of_bounds(self):
        wav(self.root/'guide.wav',1)
        save(self.root,'audio-plan.json',{'schema_version':'1.0','project_id':'coffee','version':1,'audio_mode':'narration','stage':'scratch','path':'guide.wav','duration_s':1,'timing_basis':'measured','cues':[{'cue_id':'A1','beat_ids':['B01'],'start_s':0,'end_s':3,'text':'Hello'}]})
        self.assertTrue(any('exceeds measured audio' in e for e in self.errors()))
    def test_cli_init_refuses_overwrite(self):
        cmd=['python3',str(SKILLS/'video-workflow/scripts/project.py'),'init',str(self.root),'--id','other','--format','short','--platform','tiktok','--idea','X','--duration','20']
        before=(self.root/'project.json').read_bytes()
        result=subprocess.run(cmd,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertEqual((self.root/'project.json').read_bytes(),before)


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'ffmpeg required')
class AnimaticChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        _,_,self.edit=fixture(self.root)
    def tearDown(self):
        self.tmp.cleanup()
    def render(self):
        return animatic.render(self.root/'edit-plan.json',self.root/'preview.mp4')
    def test_real_render_audio_timing_and_frame_order(self):
        wav(self.root/'guide.wav',1.5)
        self.edit['audio_path']='guide.wav'
        save(self.root,'edit-plan.json',self.edit)
        result=self.render()
        self.assertAlmostEqual(result['duration_s'],2,delta=.1)
        meta=animatic.probe(self.root/'preview.mp4','ffprobe')
        self.assertTrue(any(s['codec_type']=='audio' for s in meta['streams']))
        video=next(s for s in meta['streams'] if s['codec_type']=='video')
        self.assertEqual((video['width'],video['height']),(320,180))
        for t,winner in [(.2,0),(.7,2),(1.2,0),(1.7,2)]:
            raw=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(self.root/'preview.mp4'),'-frames:v','1','-vf','crop=2:2:160:90','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],capture_output=True,check=True).stdout
            self.assertGreater(raw[winner],180)
        with self.assertRaisesRegex(ValueError,'output exists'):
            self.render()
    def test_long_audio_rejected_before_render(self):
        wav(self.root/'long.wav',3)
        self.edit['audio_path']='long.wav'
        save(self.root,'edit-plan.json',self.edit)
        with self.assertRaisesRegex(ValueError,'exceeds timeline'):
            self.render()
        self.assertFalse((self.root/'preview.mp4').exists())
    def test_final_mode_rejected(self):
        self.edit['mode']='final'
        save(self.root,'edit-plan.json',self.edit)
        with self.assertRaisesRegex(ValueError,'animatic only'):
            self.render()
    def test_unsupported_overlay_rejected(self):
        self.edit['overlays']=['Something']
        save(self.root,'edit-plan.json',self.edit)
        with self.assertRaisesRegex(ValueError,'unsupported plan'):
            self.render()
    def test_media_path_escape_rejected(self):
        self.edit['segments'][0]['start_frame']='../image.ppm'
        save(self.root,'edit-plan.json',self.edit)
        with self.assertRaisesRegex(ValueError,'escapes project'):
            self.render()


if __name__=='__main__':
    unittest.main(verbosity=2)
