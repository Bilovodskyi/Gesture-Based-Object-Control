import { useGLTF, useTexture } from "@react-three/drei";
import { forwardRef } from "react";
import * as THREE from "three";

const metalMaterial = new THREE.MeshStandardMaterial({
    roughness: 0.3,
    metalness: 1,
    color: "#bbbbbb",
});

export const CokeCan = forwardRef((props, ref) => {
    const { nodes } = useGLTF("/can/Soda-can.gltf");
    const label = useTexture("/labels/original.png");
    label.flipY = false;
    return (
        <group dispose={null} scale={2} rotation={[0, -Math.PI, 0]} ref={ref}>
            <mesh
                castShadow
                receiveShadow
                geometry={nodes.cylinder.geometry}
                material={metalMaterial}
            />
            <mesh castShadow receiveShadow geometry={nodes.cylinder_1.geometry}>
                <meshStandardMaterial
                    roughness={0.25}
                    metalness={0.7}
                    map={label}
                />
            </mesh>
            <mesh
                castShadow
                receiveShadow
                geometry={nodes.Tab.geometry}
                material={metalMaterial}
            />
        </group>
    );
});

useGLTF.preload("/can/Soda-can.gltf");
