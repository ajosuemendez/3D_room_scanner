import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls';
import { PLYLoader } from 'three/addons/loaders/PLYLoader';
import Stats from 'three/addons/libs/stats.module';

var splitUrl = window.location.href.split('/');
console.log(splitUrl) //getUrl for filename "/"+splitUrl[4]+"/"+splitUrl[5] /models/filename
splitUrl =  "/models/ply/"+splitUrl.at(-1) //"/models/ply/cloud2.ply";
const scene = new THREE.Scene()
scene.add(new THREE.AxesHelper(5))

const light = new THREE.SpotLight()
light.position.set(20, 20, 20)
scene.add(light)

const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
)
camera.position.z = 40

const renderer = new THREE.WebGLRenderer()
renderer.outputEncoding = THREE.sRGBEncoding
renderer.setSize(window.innerWidth, window.innerHeight)
document.body.appendChild(renderer.domElement)

const controls = new OrbitControls(camera, renderer.domElement)
controls.enableDamping = true

const material = new THREE.MeshPhysicalMaterial({
    color: 0xb2ffc8,
    metalness: 0,
    roughness: 0,
    transparent: true,
    transmission: 1.0,
    side: THREE.DoubleSide,
    clearcoat: 1.0,
    clearcoatRoughness: 0.25
})

const loader = new PLYLoader()
loader.load(
    splitUrl,
    function (geometry) {
      var material = new THREE.PointsMaterial( { size: 0.005 } );
      material.vertexColors = true //if has colors geometry.attributes.color.count > 0
      var mesh = new THREE.Points(geometry, material)
      scene.add(mesh)
    },
    (xhr) => {
        console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
    },
    (error) => {
        console.log(error)
    }
)

window.addEventListener('resize', onWindowResize, false)
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
    render()
}

const stats = Stats()
stats.domElement.style.cssText = 'position:absolute;top:15vh;left:1.5vh;';
document.body.appendChild(stats.dom)

function animate() {
    requestAnimationFrame(animate)

    controls.update()

    render()

    stats.update()
}

function render() {
    renderer.render(scene, camera)
}

animate()