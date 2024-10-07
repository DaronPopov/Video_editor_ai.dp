document.addEventListener('DOMContentLoaded', function() {
    // Set up Three.js for 3D canvas
    const container = document.getElementById('threeDContainer');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableZoom = true;

    // Example Cube for testing
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
    camera.position.z = 5;

    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();

    // Handle File Upload
    const showUploadFormButton = document.getElementById('showUploadForm');
    const uploadModal = document.getElementById('uploadModal');
    const closeUploadModalButton = document.getElementById('closeUploadModal');
    const uploadForm = document.getElementById('uploadMediaForm');
    const mediaFileInput = document.getElementById('mediaFileInput');

    showUploadFormButton.addEventListener('click', () => {
        uploadModal.classList.add('is-active');
    });

    closeUploadModalButton.addEventListener('click', () => {
        uploadModal.classList.remove('is-active');
    });

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const file = mediaFileInput.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            axios.post('/upload', formData)
                .then(response => {
                    console.log(response.data);
                    // Handle success, display video/image in container
                })
                .catch(error => {
                    console.error(error);
                });
        }
    });

    // Dark Mode Toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    darkModeToggle.addEventListener('change', function() {
        if (darkModeToggle.checked) {
            document.body.classList.add('dark-mode');
            document.body.classList.remove('light-mode');
        } else {
            document.body.classList.add('light-mode');
            document.body.classList.remove('dark-mode');
        }
    });

    // Reset Canvas
    const resetCanvasButton = document.getElementById('resetCanvasButton');
    resetCanvasButton.addEventListener('click', () => {
        scene.clear();
    });
});
