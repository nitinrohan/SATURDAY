import React, { useRef, useEffect } from "react";
import styled from "styled-components";
import * as THREE from "three";

const Canvas = styled.canvas`
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
`;

/**
 * A calm, "3D presence": a slowly breathing wireframe icosahedron, a soft glow,
 * a drifting starfield and two coloured lights that parallax to the pointer/scroll.
 * Falls back to nothing (CSS aurora shows through) if reduced-motion is requested.
 */
const SceneBackground = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x06060d, 0.06);

    const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 100);
    camera.position.set(0, 0, 8);

    const geo = new THREE.IcosahedronGeometry(2.4, 2);
    const mesh = new THREE.Mesh(
      geo,
      new THREE.MeshStandardMaterial({
        color: 0x8b5cf6,
        wireframe: true,
        transparent: true,
        opacity: 0.55,
        emissive: 0x4c1d95,
        emissiveIntensity: 0.6,
        roughness: 0.4,
      })
    );
    scene.add(mesh);

    const glow = new THREE.Mesh(
      new THREE.SphereGeometry(1.5, 32, 32),
      new THREE.MeshBasicMaterial({ color: 0x22d3ee, transparent: true, opacity: 0.08 })
    );
    scene.add(glow);

    const l1 = new THREE.PointLight(0x22d3ee, 2, 40);
    l1.position.set(6, 4, 6);
    const l2 = new THREE.PointLight(0xf472b6, 2, 40);
    l2.position.set(-6, -3, 4);
    scene.add(l1, l2, new THREE.AmbientLight(0x404060, 1.2));

    const starGeo = new THREE.BufferGeometry();
    const count = 900;
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count * 3; i++) pos[i] = (Math.random() - 0.5) * 40;
    starGeo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const stars = new THREE.Points(
      starGeo,
      new THREE.PointsMaterial({ color: 0x9ca3ff, size: 0.05, transparent: true, opacity: 0.7 })
    );
    scene.add(stars);

    const pointer = { x: 0, y: 0 };
    let scrollY = 0;
    const onPointer = (e) => {
      pointer.x = (e.clientX / window.innerWidth - 0.5) * 2;
      pointer.y = (e.clientY / window.innerHeight - 0.5) * 2;
    };
    const onScroll = () => {
      scrollY = window.scrollY;
    };
    const resize = () => {
      const w = window.innerWidth;
      const h = window.innerHeight;
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    };
    window.addEventListener("pointermove", onPointer);
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", resize);
    resize();

    const base = geo.attributes.position.array.slice();
    const clock = new THREE.Clock();
    let raf;

    const tick = () => {
      const t = clock.getElapsedTime();

      const arr = geo.attributes.position.array;
      for (let i = 0; i < arr.length; i += 3) {
        const nx = base[i];
        const ny = base[i + 1];
        const nz = base[i + 2];
        const f = 1 + 0.06 * Math.sin(t * 1.2 + nx * 2 + ny * 2);
        arr[i] = nx * f;
        arr[i + 1] = ny * f;
        arr[i + 2] = nz * f;
      }
      geo.attributes.position.needsUpdate = true;

      mesh.rotation.y = t * 0.15;
      mesh.rotation.x = t * 0.08;
      glow.scale.setScalar(1 + 0.08 * Math.sin(t * 1.5));
      stars.rotation.y = t * 0.02;

      camera.position.x += (pointer.x * 1.2 - camera.position.x) * 0.04;
      camera.position.y += (-pointer.y * 1.2 - scrollY * 0.0016 - camera.position.y) * 0.04;
      camera.lookAt(0, 0, 0);

      renderer.render(scene, camera);
      raf = requestAnimationFrame(tick);
    };
    tick();

    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("pointermove", onPointer);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", resize);
      geo.dispose();
      glow.geometry.dispose();
      starGeo.dispose();
      renderer.dispose();
    };
  }, []);

  return <Canvas ref={canvasRef} aria-hidden="true" />;
};

export default SceneBackground;
