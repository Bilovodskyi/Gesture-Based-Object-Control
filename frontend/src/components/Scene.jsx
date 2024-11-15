import { useEffect, useRef, useState } from "react";

import { Environment, OrbitControls } from "@react-three/drei";
import { CokeCan } from "./CokeCan";

import * as THREE from "three";

export const Scene = () => {
    const [position, setPosition] = useState({
        rotationX: 0,
        rotationY: 0,
        positionX: 0,
        positionY: 0,
    });

    const canRef = useRef(null);
    const canGroupRef = useRef(null);
    const controlRef = useRef(null);

    useEffect(() => {
        const socket = new WebSocket("ws://localhost:6789");

        socket.onopen = () => {
            console.log("Connected to WebSocket server");
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setPosition((prev) => ({
                rotationX: prev.rotationX + data.rotation_x * 2,
                rotationY: prev.rotationY + data.rotation_y * 2,
                positionX: prev.positionX + data.position_x * 1.5,
                positionY: prev.positionY + data.position_y * 1.5,
            }));
        };

        socket.onclose = () => {
            console.log("Disconnected from WebSocket server");
        };

        return () => {
            socket.close();
        };
    }, []);

    useEffect(() => {
        if (canRef.current) {
            canRef.current.rotation.y = position.rotationX;
            canRef.current.rotation.x = position.rotationY;
            canRef.current.position.x = position.positionX;
            canRef.current.position.y = -position.positionY;
        }
    }, [position]);

    console.log(position);

    return (
        <group ref={canGroupRef}>
            <CokeCan ref={canRef} />
            <OrbitControls
                makeDefault
                ref={controlRef}
                enableZoom={false}
                enablePan={false}
                rotateSpeed={0.4}
                target={new THREE.Vector3(0, 0, 0)}
            />
            <Environment
                files="/hdr/lebombo_1k.hdr"
                environmentIntensity={1.25}
            />
        </group>
    );
};
