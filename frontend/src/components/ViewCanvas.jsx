import { Loader } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";
import { Scene } from "./Scene";

export default function ViewCanvas() {
    return (
        <>
            <Canvas
                style={{
                    position: "fixed",
                    top: 0,
                    left: "50%",
                    transform: "translateX(-50%)",
                    overflow: "hidden",
                    zIndex: 9999,
                }}
                shadows
                dpr={[1, 1.5]}
                gl={{ antialias: true }}
                camera={{
                    fov: 30,
                }}>
                <Suspense fallback={null}>
                    <Scene />
                </Suspense>
            </Canvas>
            <Loader />
        </>
    );
}
