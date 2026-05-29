convenção não fixa de ids/logging  
pai:pai:pai:filho  
actions:16  
actions:symbolic  
  
exemplo da cli  
```bash
-> python3 -m src.copykit map -mf "mimetypes.json"
mimetypes > entry
mimetypes key: script
mimetypes (entry:script) > new
mimetypes (entry:script) substitute: script
mimetypes (entry:script) canonical: text-x-script
mimetypes (entry:script) changelog:
mimetypes (entry:script) > target
icon: text-x-script
action: replace
mimetypes (entry:script) > ..
mimetypes > entry
mimetypes key: python
mimetypes (entry:python) > new
mimetypes (entry:python) substitute: python
mimetypes (entry:python) canonical: text-x-python
mimetypes (entry:python) changelog: made one of the snakes translucent
mimetypes (entry:python) > target
icon: text-x-python
action: replace
mimetypes (entry:python) > source
source: MOREWAITA
used: symbol and background color
(single) asset: scalable/mimetypes/text-x-python
mimetypes (entry:python) > ..
mimetypes > exit
```