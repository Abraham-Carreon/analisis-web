$path = "./investigacion" 

If(!(test-path -PathType container $path)) { New-Item -ItemType Directory -Path $path }

echo "Ya casi termina...."

cd investigacion

New-Item -ItemType HardLink -Path "./investigacionDominio.json" -Value "../investigacionDominio.json" -Force
New-Item -ItemType HardLink -Path "./metaimagenes.json" -Value "../metaimagenes.json" -Force
New-Item -ItemType HardLink -Path "./metapdfs.json" -Value "../metapdfs.json" -Force
New-Item -ItemType HardLink -Path "./investigacionTecnologias.json" -Value "../investigacionTecnologias.json" -Force

echo ""
echo "Terminado!"