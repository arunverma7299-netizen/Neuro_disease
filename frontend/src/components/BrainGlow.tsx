import { useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import { Float, OrbitControls, Sphere, useCursor, Sparkles } from '@react-three/drei';
import * as THREE from 'three';

type BrainGlowProps = {
  score: number;
  scanStarted: boolean;
};

const intensityByScore = (score: number) => {
  if (score <= 30) return 0.25;
  if (score <= 50) return 0.45;
  if (score <= 70) return 0.7;
  return 0.95;
};

function StylizedBrain({ intensity }: { intensity: number }) {
  const color = useMemo(() => new THREE.Color(`#7dd3fc`).lerp(new THREE.Color('#f97316'), intensity * 0.65), [intensity]);
  return (
    <Float speed={1.2} rotationIntensity={0.45} floatIntensity={0.55}>
      <mesh>
        <sphereGeometry args={[1.2, 32, 32]} />
        <meshStandardMaterial color={color} roughness={0.35} metalness={0.25} emissive={color} emissiveIntensity={0.5 + intensity * 0.4} />
      </mesh>
      <mesh position={[-0.35, 0.12, 0.15]} scale={[0.72, 0.95, 0.7]}>
        <sphereGeometry args={[0.9, 24, 24]} />
        <meshStandardMaterial color={color} roughness={0.4} metalness={0.15} emissive={color} emissiveIntensity={0.35 + intensity * 0.3} />
      </mesh>
      <mesh position={[0.38, 0.1, -0.1]} scale={[0.75, 0.9, 0.68]}>
        <sphereGeometry args={[0.9, 24, 24]} />
        <meshStandardMaterial color={color} roughness={0.4} metalness={0.15} emissive={color} emissiveIntensity={0.35 + intensity * 0.3} />
      </mesh>
      <Sparkles count={intensity > 0.7 ? 70 : 36} scale={[3.2, 3.2, 3.2]} size={3} speed={0.65} color={intensity > 0.7 ? '#f8fafc' : '#67e8f9'} />
      <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, -1.6, 0]}>
        <ringGeometry args={[1.35, 1.55, 48]} />
        <meshBasicMaterial color="#67e8f9" transparent opacity={0.3 + intensity * 0.35} side={THREE.DoubleSide} />
      </mesh>
    </Float>
  );
}

export function BrainGlow({ score, scanStarted }: BrainGlowProps) {
  const intensity = intensityByScore(score);
  const pulse = scanStarted ? 1 + intensity * 0.18 : 1;

  return (
    <div className="brain-canvas-shell" aria-hidden="true">
      <Canvas camera={{ position: [0, 0, 4.2], fov: 42 }}>
        <color attach="background" args={['#050816']} />
        <ambientLight intensity={0.85} />
        <pointLight position={[2, 2, 3]} intensity={1.8} color="#67e8f9" />
        <pointLight position={[-2, -1, 2]} intensity={1.2} color="#f97316" />
        <group scale={pulse}>
          <StylizedBrain intensity={intensity} />
        </group>
        <OrbitControls enablePan={false} enableZoom={false} autoRotate autoRotateSpeed={0.65 + intensity * 0.4} />
      </Canvas>
      <div className="brain-caption">
        <span>Neural intensity</span>
        <strong>{score} / 100</strong>
      </div>
    </div>
  );
}
