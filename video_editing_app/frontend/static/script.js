document.addEventListener('DOMContentLoaded', function() {
    // Set up WebGPU for 3D canvas
    const container = document.getElementById('threeDContainer');
    const adapter = await navigator.gpu.requestAdapter();
    const device = await adapter.requestDevice();
    const context = container.getContext('webgpu');
    const format = navigator.gpu.getPreferredCanvasFormat();
    context.configure({
        device: device,
        format: format,
        alphaMode: 'opaque'
    });

    // Vertex shader
    const vertexShaderCode = `
        @vertex
        fn main(@builtin(vertex_index) VertexIndex : u32) -> @builtin(position) vec4<f32> {
            var pos = array<vec2<f32>, 3>(
                vec2<f32>(0.0, 0.5),
                vec2<f32>(-0.5, -0.5),
                vec2<f32>(0.5, -0.5)
            );
            return vec4<f32>(pos[VertexIndex], 0.0, 1.0);
        }
    `;

    // Fragment shader
    const fragmentShaderCode = `
        @fragment
        fn main() -> @location(0) vec4<f32> {
            return vec4<f32>(1.0, 0.0, 0.0, 1.0);
        }
    `;

    const shaderModule = device.createShaderModule({
        code: vertexShaderCode + fragmentShaderCode
    });

    const pipeline = device.createRenderPipeline({
        vertex: {
            module: shaderModule,
            entryPoint: 'main'
        },
        fragment: {
            module: shaderModule,
            entryPoint: 'main',
            targets: [{
                format: format
            }]
        },
        primitive: {
            topology: 'triangle-list'
        }
    });

    const commandEncoder = device.createCommandEncoder();
    const textureView = context.getCurrentTexture().createView();
    const renderPassDescriptor = {
        colorAttachments: [{
            view: textureView,
            loadValue: { r: 0.0, g: 0.0, b: 0.0, a: 1.0 },
            storeOp: 'store'
        }]
    };

    const passEncoder = commandEncoder.beginRenderPass(renderPassDescriptor);
    passEncoder.setPipeline(pipeline);
    passEncoder.draw(3, 1, 0, 0);
    passEncoder.endPass();

    device.queue.submit([commandEncoder.finish()]);

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
