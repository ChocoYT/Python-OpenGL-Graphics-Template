#version 460 core

in vec3 vPosition;
in vec4 vColor;
in vec3 vNormal;

out vec4 fragColor;

void main()
{
    fragColor = vColor;
}
