import os, json
base='/home/claude/dyno-site'
files={}
for d,_,fs in os.walk(base+'/www'):
    for f in fs:
        p=os.path.join(d,f); rel=os.path.relpath(p,base+'/www'); files[rel]=open(p,encoding='utf-8').read()
nginx=open(base+'/deploy/nginx.conf').read()
def esc(s): return s.replace('$','$$')
cfg={}; mounts=[]
for i,(rel,c) in enumerate(sorted(files.items())):
    k='site_%02d'%i; cfg[k]={'content':esc(c)}; mounts.append({'source':k,'target':'/usr/share/nginx/html/'+rel})
cfg['site_nginx']={'content':esc(nginx).replace('$${SITE_SECRET}','${SITE_SECRET}')}
mounts.append({'source':'site_nginx','target':'/etc/nginx/conf.d/default.conf'})
compose={'name':'dyno-site','services':{'dyno-site':{'image':'nginx:1.27-alpine','container_name':'dyno-site','restart':'unless-stopped','configs':mounts,
 'networks':['n8n_default'],'healthcheck':{'test':['CMD','wget','-qO-','http://127.0.0.1/']},
 'labels':{'traefik.enable':'true','traefik.docker.network':'n8n_default',
  'traefik.http.routers.dynosite.rule':'Host(`dynoapp.com.br`) || Host(`www.dynoapp.com.br`)',
  'traefik.http.routers.dynosite.entrypoints':'websecure','traefik.http.routers.dynosite.tls':'true',
  'traefik.http.routers.dynosite.tls.certresolver':'mytlschallenge','traefik.http.services.dynosite.loadbalancer.server.port':'80'},
 'logging':{'driver':'json-file','options':{'max-size':'10m','max-file':'3'}}}},
 'configs':cfg,'networks':{'n8n_default':{'external':True}}}
import yaml
out=yaml.safe_dump(compose,allow_unicode=True,sort_keys=False,width=100000)
open(base+'/deploy/docker-compose.yml','w').write(out)
print(len(out))
