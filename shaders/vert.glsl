#version 460 core

uniform mat4 uCameraProjMatrix;
uniform mat4 uCameraViewMatrix;

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec4 aColor;
layout (location = 2) in vec3 aNormal;

out vec3 vPosition;
out vec4 vColor;
out vec3 vNormal;

void main()
{
    gl_Position = uCameraProjMatrix * uCameraViewMatrix * vec4(aPosition, 1.0);

    vPosition = aPosition;
    vColor    = aColor;
    vNormal   = aNormal;
}
