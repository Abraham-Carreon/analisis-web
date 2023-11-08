$path = "./investigacion" 

If(!(test-path -PathType container $path)) { New-Item -ItemType Directory -Path $path }

echo "Ya casi termina...."

cd investigacion

New-Item -ItemType HardLink -Path "./investigacionDominio.json" -Target "../investigacionDominio.json"
New-Item -ItemType HardLink -Path "./metaimagenes.json" -Target "../metaimagenes.json"
New-Item -ItemType HardLink -Path "./metapdfs.json" -Target "../metapdfs.json"
New-Item -ItemType HardLink -Path "./investigacionTecnologias.json" -Target "../investigacionTecnologias.json"

echo ""
echo "Terminado!"