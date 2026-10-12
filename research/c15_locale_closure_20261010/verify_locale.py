"""Model-free locale dependency verification; byte matches never grant admission."""
import sys
INITIAL_MODULES=tuple(sys.modules)
ALLOWED_MODULE_NAMES = ('__main__', '_abc', '_ast', '_bisect', '_blake2', '_codecs', '_collections', '_collections_abc', '_frozen_importlib', '_frozen_importlib_external', '_functools', '_hashlib', '_imp', '_io', '_json', '_opcode', '_opcode_metadata', '_operator', '_random', '_signal', '_sre', '_stat', '_struct', '_thread', '_tokenize', '_types', '_warnings', '_weakref', '_weakrefset', 'abc', 'annotationlib', 'ast', 'bisect', 'builtins', 'codecs', 'collections', 'collections.abc', 'copy', 'copyreg', 'dataclasses', 'dis', 'encodings', 'encodings.aliases', 'encodings.utf_8', 'enum', 'errno', 'functools', 'genericpath', 'hashlib', 'importlib', 'importlib._bootstrap', 'importlib._bootstrap_external', 'importlib.machinery', 'inspect', 'io', 'itertools', 'json', 'json.decoder', 'json.encoder', 'json.scanner', 'keyword', 'linecache', 'marshal', 'math', 'opcode', 'operator', 'os', 'os.path', 'posix', 'posixpath', 'random', 're', 're._casefix', 're._compiler', 're._constants', 're._parser', 'reprlib', 'stat', 'struct', 'sys', 'time', 'token', 'tokenize', 'types', 'weakref', 'zipimport')
def operation_guard(event,args):
 if event=='import' and (args[0] not in ALLOWED_MODULE_NAMES or args[0]=='sparkbrain' or args[0].startswith('sparkbrain.')): raise RuntimeError('UNDECLARED_IMPORT')
 if event.startswith(('socket.','subprocess.','os.exec','os.spawn','os.fork')): raise RuntimeError('FORBIDDEN_OPERATION')
sys.addaudithook(operation_guard)
import os, json, hashlib, types, importlib.machinery
REFERENCE_ROWS = (('/opt/hostedtoolcache/Python/3.14.8/x64/bin/python3.14', 17752, 'a5230d8adbd26c2185d77fb003597c4ee9c44c2369fc179122ff7c3a3a58ae59'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/libpython3.14.so.1.0', 32414720, 'ce19367f84f6a9f096c0ccd2047aba8197101e5637e065471235aed8df7cbb3c'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/_opcode_metadata.py', 10115, 'd9badc5ab19a66415e230bf8f4299491b2207d584981a92b6e7c447cfa1aeac3'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/_weakrefset.py', 3962, '2dd7cb459d654fe78b00c5c47ee8e786c037ee77763304603f5e976dd62cbf81'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/annotationlib.py', 44420, '1cce29393714b91e3f71571ffbedacc7f73f11ad26be10701debeb86ec059a32'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/ast.py', 25479, '5ea9a796353544bea0d706153516f04ef3d92be305d15a73238403837d77e34c'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/bisect.py', 3423, 'f1cf7b85fc36b5da249813fc5ab97d9464f8cc1bc817f7146206fa2713e35999'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/collections/__init__.py', 53021, 'cb8367b8edd188662143ea2e3942d360c2deae51c72fd779ec898f5076d2c2b9'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/copy.py', 8582, '15154fde290d6e65b5007905689a47a9a5a724822c5e06eec35d9ffbb2a3aa69'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/copyreg.py', 7716, '6376eb5722806396f5842997ac18add369ea9ac3ff4fcfe1460c41a088cac425'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/dataclasses.py', 71537, 'e8439c8b111856645a8b31e0dbbba532b494426399bad456079c0e5730ad322e'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/dis.py', 45533, '17d4d9a9195c9ee5aa27a96f3e0871f9363fd501e3a64ef20cb1cc876d7ad553'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/encodings/__init__.py', 5945, '2b708410495acf12a6fad9d2de928dd89e567537c253eaa2b51aaae578e96c59'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/encodings/aliases.py', 16255, '1ee993f8eb4986999b6501381e53947be9a04443626cb48b4190bcff2e87d3b4'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/encodings/utf_8.py', 1005, 'ba0cac060269583523ca9506473a755203037c57d466a11aa89a30a5f6756f3d'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/enum.py', 85450, 'fd23a7598fa1104ef892abcd4154d3627283e6361eb7a91cd11dc4a7b6fb3a93'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/functools.py', 43564, '9db56d38172c4c9e689b21cc58c8538008b09d86b682faf4dd193b529cdd79d5'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/hashlib.py', 9459, '88fa624821fbdee7eb2ef87c2437b207afe328cf117c7463367e2db5eb1af492'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/importlib/__init__.py', 4767, '72b07de4133a7e39b2f6a7920465669aa04626f217e800779587bc0713fe002e'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/inspect.py', 128112, '6daf297029d8971703b344de5cd485d71d4d935c72b85591493d8abc8512bdf7'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/json/__init__.py', 14132, '2dd10f1bf4c9ea5478e589216805e7f279d0e4bce134a19efa297404fb87407d'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/json/decoder.py', 12877, 'dc98d3e677612ea7311303f06a144cec6b91ebadc7ec037d1777501647578a07'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/json/encoder.py', 16990, 'd68a4d04d2cfd95897498307f29349058b42c3f48ea6aa6739714a09200a7d01'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/json/scanner.py', 2434, '572958017eae8842eeddd0e3d18d3c56cc0a197348224915e1d87ce937841764'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/keyword.py', 1073, '18c2be738c04ad20ad375f6a71db34b3823c7f40b0340f5294d0e89f3c9b093b'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/lib-dynload/_bisect.cpython-314-x86_64-linux-gnu.so', 97208, '7b1a98e752b2e37528e8f8c066114348c2c86f2c5cb01aca1866b54d826148b1'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/lib-dynload/_blake2.cpython-314-x86_64-linux-gnu.so', 1705672, '27f5117c356ebc44e823a7027174c1db6929ab5949ffa871d564bf4e31aa4faa'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/lib-dynload/_hashlib.cpython-314-x86_64-linux-gnu.so', 337032, '2abe527b9cc50ffe7e363b068a499ad7b344ce7ed815ff92cffe9c80bd5de272'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/lib-dynload/_json.cpython-314-x86_64-linux-gnu.so', 342328, 'dd1230c15ef4c470131a34a8dac45190dade4b2759e1e5c5c59d33a0b3a82a68'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/lib-dynload/_random.cpython-314-x86_64-linux-gnu.so', 60072, '2838acd7040a5de39155eb79bfd4df7dd12c789cc2930e4977381b135fb522ee'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/lib-dynload/_struct.cpython-314-x86_64-linux-gnu.so', 258560, '82bb2522e04548ebf382d454dfe406200b12330af750cb43ed3fd9c16e90f5ca'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/lib-dynload/math.cpython-314-x86_64-linux-gnu.so', 429880, 'abd6228819f15f9d2ea5b861f54dfb59c902da51465f472cb0c9b1e839757fef'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/linecache.py', 8044, '692daec68e2a419adf46bafc0eb2f8a2fb36c482183fa1ac47e00fec440f7d7e'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/opcode.py', 3152, '1036d90c917bb27c540ac3205d22896ee747214df1f2682458ab915758e4fdf2'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/operator.py', 11158, 'a9f9910965c31f841caad0447ee47299ac539a371422aefe200c86c60f3b4697'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/random.py', 37553, 'cf8e72f887d838e273c274b79758b2bf8630a0927112b8876fa3a9e4b9b1756b'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/re/__init__.py', 17876, '741a9de729ed8207bfa19db990f8826f1bf3661f33d0970a80c08cd1338ebc35'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/re/_casefix.py', 5444, '1b12d9136f23db6c3f6f26053fefc15ca964b886838c7b9c1fabf8d2efc1e5c8'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/re/_compiler.py', 26855, 'd49f30cf9a1dbae33b200ed8befd9d0ce3ac612783a10ac35196536f98923e91'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/re/_constants.py', 6036, '42253b3181b81aad6c46392f44a0ab26dcfa31feea411296f43ba16616a1ab0b'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/re/_parser.py', 40353, 'e57bd194a2d42398355ae7c1ccc2ddfb78421dd431eb81e3809dbe8ca9057dc4'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/reprlib.py', 8064, 'b04872e10d76252e44eae50cc785eb0fe478491afc4d7f0825a93f82b2eaba5f'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/struct.py', 285, '50c14e55f94957804c1e45e975fedbe8e86f7e1dbb745b150370ff681155370a'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/token.py', 2584, '61d4270311099c8a0c0b2e45fb363fd1c4e347a720bcc25f682b63dc28c34234'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/tokenize.py', 21849, '65ba1bacdc42e768382208ff27f3001ee77d9d61aafba686c67652d22b84b330'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/types.py', 11464, '8c54d3d5ffc1d1204237e6c69b25c27c7b05b483128f185eeed9ba7ef2229ac2'), ('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/weakref.py', 17771, '5e5f727a19a858cb4c56dbaf3e0a138ded02fb954a9a58a840a0764216ae9522'), ('/usr/lib/locale/C.utf8/LC_CTYPE', 360460, '59015993b1b671273461ef1167d7a9ad76dc090d521c91102e962217ed6b6dba'), ('/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache', 27028, '52c227df9d53248238602c1ddaccd2c8ddc4cc6a61aa45d7c425af590b8806a5'), ('/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2', 236616, 'c20a2dc8917c755f02b94049356320fe1f62ac7d9f8994731f807d9df39302da'), ('/usr/lib/x86_64-linux-gnu/libc.so.6', 2129424, '3a15d66867d83762c7f2f1e37359cb8f6c5743edb369c65285cb0b1c4f7498bf'), ('/usr/lib/x86_64-linux-gnu/libcrypto.so.3', 5309400, '6866ed711dab8927e1bf82bf1cd30e828bdfc34f3cc1e83b1c9eb01ce6c37d9a'), ('/usr/lib/x86_64-linux-gnu/libm.so.6', 952616, 'fce00b6f25f459cf4ae0b7fae4257909a1a8a86f9149e7c029a5d617baf1ccd0'))
MAX_READ=64*1024*1024
MAX_FILE=32*1024*1024
MAX_MAPS=1024*1024
MAX_OUTPUT=1024*1024
PRELOAD=('copy','copyreg','dataclasses','random','inspect')
READ_BYTES=0
CLAIMS={'native_admission':False,'trusted_pins_approved':False,'scientific_execution':False,'complete_executed_code_provenance':False,'owner_constructions':0,'native_query_calls':0}

def need(ok,why):
 if not ok: raise RuntimeError(why)

def read_file(path,cap,expected_identity=None):
 global READ_BYTES
 need(type(path) is str and path.startswith('/') and all(p not in ('','.','..') for p in path.split('/')[1:]),'NONCANONICAL_PATH')
 fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:
  for component in path.split('/')[1:-1]:
   nxt=os.open(component,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=nxt
  leaf=os.open(path.split('/')[-1],os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=fd)
 finally: os.close(fd)
 try:
  before=os.fstat(leaf); need(before.st_mode&0o170000==0o100000 and 0<=before.st_size<=cap,'FILE_TYPE_SIZE')
  if expected_identity is not None: need((os.major(before.st_dev),os.minor(before.st_dev),before.st_ino)==expected_identity,'MAPPED_FILE_IDENTITY')
  chunks=[];total=0
  while True:
   data=os.read(leaf,min(65536,cap+1-total))
   if not data: break
   total+=len(data);READ_BYTES+=len(data);need(total<=cap and READ_BYTES<=MAX_READ,'READ_LIMIT');chunks.append(data)
  after=os.fstat(leaf)
  need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns),'FILE_CHANGED')
  return b''.join(chunks),before
 finally: os.close(leaf)

def maps(stage,reference,identities):
 global READ_BYTES
 with open('/proc/self/maps','rb') as source: raw=source.read(MAX_MAPS+1)
 READ_BYTES+=len(raw);need(len(raw)<=MAX_MAPS and READ_BYTES<=MAX_READ,'MAPS_READ_LIMIT')
 lines=raw.decode('ascii').splitlines();need(len(lines)<=4096,'MAP_COUNT')
 files={}; special=set()
 for line in lines:
  fields=line.split(None,5);need(len(fields) in (5,6),'MAP_SHAPE')
  permissions=fields[1];need(len(permissions)==4 and not ('w' in permissions and 'x' in permissions),'WRITABLE_EXECUTABLE_MAPPING')
  path=fields[5] if len(fields)==6 else ''
  if not path.startswith('/'):
   kernel_exec=(path=='[vdso]' and permissions=='r-xp') or (path=='[vsyscall]' and permissions=='--xp' and fields[0]=='ffffffffff600000-ffffffffff601000')
   need('x' not in permissions or kernel_exec,'UNDECLARED_EXECUTABLE_MAPPING');special.add(path if path in ('','[heap]','[stack]','[vdso]','[vvar]','[vvar_vclock]','[vsyscall]') else 'OTHER_NONEXECUTABLE_PSEUDOMAP');continue
  need(not path.endswith(' (deleted)'),'DELETED_MAPPING')
  need(path!='/usr/lib/locale/locale-archive','GENERATED_LOCALE_ARCHIVE_MAPPED')
  need(path in reference,'UNDECLARED_MAPPED_FILE')
  device=fields[3].split(':');need(len(device)==2,'MAP_DEVICE');ident=(int(device[0],16),int(device[1],16),int(fields[4],10))
  need(ident[2]>0 and ident==identities[path],'MAPPING_REFERENCE_IDENTITY')
  files[path]=ident
 return {'stage':stage,'mapped_files':sorted(files),'special_mapping_labels':sorted(special),'locale_archive_mapped':False}

def verify():
 need(sys.implementation.name=='cpython' and tuple(sys.version_info)==(3,14,8,'final',0),'TARGET_VERSION')
 need(sys.executable=='/opt/hostedtoolcache/Python/3.14.8/x64/bin/python3.14' and sys.base_prefix=='/opt/hostedtoolcache/Python/3.14.8/x64','TARGET_PATH')
 need(sys.abiflags=='' and sys._is_gil_enabled(),'ORDINARY_CPYTHON_REQUIRED')
 need(tuple(sys.path)==('/opt/hostedtoolcache/Python/3.14.8/x64/lib/python314.zip','/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14','/opt/hostedtoolcache/Python/3.14.8/x64/lib/python3.14/lib-dynload'),'IMPORT_SEARCH_PATH')
 need(set(sys.modules).issubset(ALLOWED_MODULE_NAMES),'UNDECLARED_INITIAL_MODULE')
 need(sys.flags.isolated==1 and sys.flags.no_site==1 and sys.flags.dont_write_bytecode==1 and sys.flags.utf8_mode==1,'STARTUP_FLAGS')
 need(os.environ.get('LC_ALL')=='C' and os.environ.get('LANG')=='C','LOCALE_ENVIRONMENT')
 need(sys.gettrace() is None and sys.getprofile() is None,'TRACE_PROFILE')
 need(not any(n=='sparkbrain' or n.startswith('sparkbrain.') for n in sys.modules),'MODEL_ALREADY_LOADED')
 reference={path:(size,digest) for path,size,digest in REFERENCE_ROWS};need(len(reference)==53,'REFERENCE_CENSUS')
 identities={};checked=[]
 for path,(size,digest) in reference.items():
  raw,st=read_file(path,MAX_FILE);need(len(raw)==size and hashlib.sha256(raw).hexdigest()==digest,'REFERENCE_BYTES_MISMATCH:'+path)
  identities[path]=(os.major(st.st_dev),os.minor(st.st_dev),st.st_ino);checked.append(path)
 del raw
 before=maps('after_support_imports',reference,identities)
 for name in PRELOAD: __import__(name)
 need(len(sys.modules)<=256 and set(sys.modules).issubset(ALLOWED_MODULE_NAMES),'MODULE_COUNT_OR_CENSUS')
 need(not any(n=='sparkbrain' or n.startswith('sparkbrain.') for n in sys.modules),'MODEL_IMPORTED')
 after=maps('after_fixed_stdlib_preload',reference,identities)
 # Retain explicit existing wrapper and its closed-over function without invoking either.
 wrapper=vars(importlib.machinery.BuiltinImporter)['get_code'].__func__
 need(type(wrapper) is types.FunctionType and wrapper.__closure__ is not None and len(wrapper.__closure__)==1,'BUILTIN_WRAPPER_LAYOUT')
 cell=wrapper.__closure__[0];target=cell.cell_contents
 need(type(target) is types.FunctionType and target.__module__=='_frozen_importlib' and target.__qualname__=='BuiltinImporter.get_code','BUILTIN_WRAPPER_TARGET')
 retained=(wrapper,wrapper.__code__,wrapper.__globals__,cell,target,target.__code__,target.__globals__)
 need(wrapper.__closure__[0] is cell and cell.cell_contents is target and wrapper.__code__ is retained[1] and target.__code__ is retained[5],'LIVE_REFERENCE_DRIFT')
 return {**CLAIMS,'status':'MODEL_FREE_DEPENDENCY_CHECK_COMPLETE','checked_official_files':checked,'mapping_checks':[before,after],'fixed_preloads':PRELOAD,'module_names':sorted(sys.modules),'explicit_read_bytes':READ_BYTES,'loader_reads_counted':False,'function_edge':{'container':'BuiltinImporter.get_code','cell_ordinal':0,'target_qualname':target.__qualname__,'same_process_reference_retained':True},'limitations':['Retained edge is structural evidence only; callable/global semantics remain unapproved.','No source/pyc/frozen execution equivalence attestation.','Mapped-file checks are snapshots under a quiescent trusted-process assumption.']}

if __name__=='__main__':
 try: result=verify();code=0
 except Exception as exc: result={**CLAIMS,'status':'INCOMPLETE','reason':str(exc) if type(exc) is RuntimeError else type(exc).__name__,'explicit_read_bytes':READ_BYTES};code=2
 encoded=json.dumps(result,sort_keys=True,separators=(',',':')).encode('ascii');need(len(encoded)<=MAX_OUTPUT,'OUTPUT_LIMIT');sys.stdout.buffer.write(encoded+b'\n');raise SystemExit(code)
