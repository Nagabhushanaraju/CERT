Prompt start

You are an expert Next.js developer. Generate a complete, production-ready interactive landing page with:

Next.js 14 (App Router), TypeScript, Tailwind CSS v4 with tw-animate-css

shadcn/ui initialised with npx shadcn@latest init (all defaults)

Components:

components/ui/globe.tsx – a draggable, auto-rotating 3D globe using cobe.
Markers include cdn-bom at coordinates [20.5937, 78.9629] (centre of India), label "🇮🇳 India".
The rotating pyramid on that marker must use the Indian tricolour: saffron (#FF9933), white (#FFFFFF), green (#138808).
The globe uses a white/light base with black markers and arcs, but the India pyramid overrides colours.
The component must export GlobeCdn with the same props and behaviour as the provided code (CDN markers, arcs, traffic labels).
components/ui/landing-page.tsx – a ScrollGlobe component that renders four scroll-driven sections and smoothly moves the globe (GlobeCdn) via CSS transforms.
Sections have titles, descriptions, features, actions.
Navigation dots on the right with auto-hiding labels.
A progress bar at the top.
Use GlobeCdn inside a fixed container that transitions between positions defined in defaultGlobeConfig.
components/background-stripes.tsx – a fixed full-screen background with:
Grid lines (40px × 40px) using hsl(var(--border)).
A soft radial glow (radial-gradient from rgba(255,249,145,0.15) to transparent) with mix-blend-mode: multiply.
components/particle-canvas.tsx – a WebGL particle trail that follows the mouse. Use the exact code below with maxParticles as a prop.
lib/utils.ts – the shadcn cn helper.
app/globals.css – Tailwind setup with light/dark variables and the fadeOutLabel keyframes.
app/layout.tsx – root layout importing globals.css, using the Inter font, and wrapping children.
app/page.tsx – the homepage that renders BackgroundStripes, ParticleCanvas (with maxParticles={5000}), and GlobeScrollDemo.
Dependencies to install (run these commands):

bash
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
npx shadcn@latest init
npm install cobe framer-motion lucide-react
File-by-file code you must produce exactly:

lib/utils.ts
ts
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }
components/ui/globe.tsx
tsx
"use client"
import { useEffect, useRef, useCallback, useState } from "react"
import createGlobe from "cobe"

interface CdnMarker { id: string; location: [number, number]; region: string }
interface CdnArc { id: string; from: [number, number]; to: [number, number] }
interface GlobeCdnProps { markers?: CdnMarker[]; arcs?: CdnArc[]; className?: string; speed?: number }

const defaultMarkers: CdnMarker[] = [
  { id: "cdn-iad", location: [38.95, -77.45], region: "iad1" },
  { id: "cdn-sfo", location: [37.62, -122.38], region: "sfo1" },
  { id: "cdn-cdg", location: [49.01, 2.55], region: "cdg1" },
  { id: "cdn-hnd", location: [35.55, 139.78], region: "hnd1" },
  { id: "cdn-syd", location: [-33.95, 151.18], region: "syd1" },
  { id: "cdn-gru", location: [-23.43, -46.47], region: "gru1" },
  { id: "cdn-sin", location: [1.36, 103.99], region: "sin1" },
  { id: "cdn-arn", location: [59.65, 17.93], region: "arn1" },
  { id: "cdn-dub", location: [53.43, -6.25], region: "dub1" },
  { id: "cdn-bom", location: [20.5937, 78.9629], region: "🇮🇳 India" }
]

const defaultArcs: CdnArc[] = [
  { id: "cdn-arc-1", from: [38.95, -77.45], to: [49.01, 2.55] },
  { id: "cdn-arc-2", from: [37.62, -122.38], to: [35.55, 139.78] },
  { id: "cdn-arc-3", from: [49.01, 2.55], to: [1.36, 103.99] },
  { id: "cdn-arc-4", from: [38.95, -77.45], to: [-23.43, -46.47] },
  { id: "cdn-arc-5", from: [35.55, 139.78], to: [-33.95, 151.18] },
  { id: "cdn-arc-6", from: [49.01, 2.55], to: [20.5937, 78.9629] }
]

export function GlobeCdn({ markers = defaultMarkers, arcs = defaultArcs, className = "", speed = 0.003 }: GlobeCdnProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const pointerInteracting = useRef<{ x: number; y: number } | null>(null)
  const dragOffset = useRef({ phi: 0, theta: 0 })
  const phiOffsetRef = useRef(0)
  const thetaOffsetRef = useRef(0)
  const isPausedRef = useRef(false)
  const [traffic, setTraffic] = useState(() => defaultArcs.map((a, i) => ({ id: a.id, value: [420, 380, 290, 185, 156, 134][i] || 100 })))

  useEffect(() => {
    const interval = setInterval(() => {
      setTraffic(data => data.map(t => ({ ...t, value: Math.max(50, t.value + Math.floor(Math.random() * 21) - 10) })))
    }, 250)
    return () => clearInterval(interval)
  }, [])

  const handlePointerDown = useCallback((e: React.PointerEvent) => {
    pointerInteracting.current = { x: e.clientX, y: e.clientY }
    if (canvasRef.current) canvasRef.current.style.cursor = "grabbing"
    isPausedRef.current = true
  }, [])

  const handlePointerUp = useCallback(() => {
    if (pointerInteracting.current !== null) {
      phiOffsetRef.current += dragOffset.current.phi
      thetaOffsetRef.current += dragOffset.current.theta
      dragOffset.current = { phi: 0, theta: 0 }
    }
    pointerInteracting.current = null
    if (canvasRef.current) canvasRef.current.style.cursor = "grab"
    isPausedRef.current = false
  }, [])

  useEffect(() => {
    const handlePointerMove = (e: PointerEvent) => {
      if (pointerInteracting.current !== null) {
        dragOffset.current = {
          phi: (e.clientX - pointerInteracting.current.x) / 300,
          theta: (e.clientY - pointerInteracting.current.y) / 1000
        }
      }
    }
    window.addEventListener("pointermove", handlePointerMove, { passive: true })
    window.addEventListener("pointerup", handlePointerUp, { passive: true })
    return () => {
      window.removeEventListener("pointermove", handlePointerMove)
      window.removeEventListener("pointerup", handlePointerUp)
    }
  }, [handlePointerUp])

  useEffect(() => {
    if (!canvasRef.current) return
    const canvas = canvasRef.current
    let globe: ReturnType<typeof createGlobe> | null = null
    let animationId: number
    let phi = 0

    function init() {
      const width = canvas.offsetWidth
      if (width === 0 || globe) return
      globe = createGlobe(canvas, {
        devicePixelRatio: Math.min(window.devicePixelRatio || 1, 2),
        width, height: width,
        phi: 0, theta: 0.2, dark: 0, diffuse: 1.5,
        mapSamples: 16000, mapBrightness: 10,
        baseColor: [1, 1, 1],
        markerColor: [0, 0, 0],
        glowColor: [0.94, 0.93, 0.91],
        markerElevation: 0.02,
        markers: markers.map(m => ({ location: m.location, size: 0.012, id: m.id })),
        arcs: arcs.map(a => ({ from: a.from, to: a.to, id: a.id })),
        arcColor: [0, 0, 0],
        arcWidth: 0.5, arcHeight: 0.25, opacity: 0.7,
      })
      function animate() {
        if (!isPausedRef.current) phi += speed
        globe!.update({
          phi: phi + phiOffsetRef.current + dragOffset.current.phi,
          theta: 0.2 + thetaOffsetRef.current + dragOffset.current.theta
        })
        animationId = requestAnimationFrame(animate)
      }
      animate()
      setTimeout(() => canvas && (canvas.style.opacity = "1"))
    }

    if (canvas.offsetWidth > 0) init()
    else {
      const ro = new ResizeObserver(entries => {
        if (entries[0]?.contentRect.width > 0) { ro.disconnect(); init() }
      })
      ro.observe(canvas)
    }

    return () => {
      if (animationId) cancelAnimationFrame(animationId)
      if (globe) globe.destroy()
    }
  }, [markers, arcs, speed])

  const pyramidFaceStyle = (nth: number, markerId?: string): React.CSSProperties => {
    const isIndia = markerId === "cdn-bom"
    const transforms = [
      "rotateY(0deg) translateZ(4px) rotateX(19.5deg)",
      "rotateY(120deg) translateZ(4px) rotateX(19.5deg)",
      "rotateY(240deg) translateZ(4px) rotateX(19.5deg)",
      "rotateX(-90deg) rotateZ(60deg) translateY(4px)"
    ]
    const colors = isIndia ? ["#FF9933", "#FFFFFF", "#138808", "#FF9933"] : ["#111", "#333", "#555", "#222"]
    return {
      position: "absolute", left: -0.5, top: 0,
      width: 0, height: 0,
      borderLeft: "6.5px solid transparent",
      borderRight: "6.5px solid transparent",
      borderBottom: `13px solid ${colors[nth]}`,
      transformOrigin: "center bottom",
      transform: transforms[nth]
    }
  }

  return (
    <div className={`relative aspect-square select-none ${className}`}>
      <style>{`@keyframes pyramid-spin { 0% { transform: rotateX(20deg) rotateY(0deg); } 100% { transform: rotateX(20deg) rotateY(360deg); } }`}</style>
      <canvas
        ref={canvasRef}
        onPointerDown={handlePointerDown}
        style={{ width: "100%", height: "100%", cursor: "grab", opacity: 0, transition: "opacity 1.2s ease", borderRadius: "50%", touchAction: "none" }}
      />
      {markers.map(m => (
        <div
          key={m.id}
          style={{
            position: "absolute",
            positionAnchor: `--cobe-${m.id}`,
            bottom: "anchor(top)",
            left: "anchor(center)",
            translate: "-50% 0",
            display: "flex", flexDirection: "column", alignItems: "center", gap: 6,
            pointerEvents: "none",
            opacity: `var(--cobe-visible-${m.id}, 0)`,
            filter: `blur(calc((1 - var(--cobe-visible-${m.id}, 0)) * 8px))`,
            transition: "opacity 0.3s, filter 0.3s"
          }}
        >
          <div style={{ width: 12, height: 12, position: "relative", transformStyle: "preserve-3d", animation: "pyramid-spin 4s linear infinite" }}>
            {[0, 1, 2, 3].map(n => <div key={n} style={pyramidFaceStyle(n, m.id)} />)}
          </div>
          <span style={{ fontFamily: "monospace", fontSize: "0.55rem", color: "#000", background: "#fff", padding: "2px 6px", borderRadius: 3, letterSpacing: "0.05em", whiteSpace: "nowrap", boxShadow: "0 1px 3px rgba(0,0,0,0.2)" }}>{m.region}</span>
        </div>
      ))}
      {traffic.map(t => (
        <div
          key={t.id}
          style={{
            position: "absolute",
            positionAnchor: `--cobe-arc-${t.id}`,
            bottom: "anchor(top)", left: "anchor(center)", translate: "-50% 0",
            fontFamily: "monospace", fontSize: "0.5rem", color: "#fff", background: "#000",
            padding: "3px 8px", borderRadius: 4, whiteSpace: "nowrap",
            pointerEvents: "none",
            opacity: `var(--cobe-visible-arc-${t.id}, 0)`,
            filter: `blur(calc((1 - var(--cobe-visible-arc-${t.id}, 0)) * 8px))`,
            transition: "opacity 0.3s, filter 0.3s"
          }}
        >{t.value}k req/s</div>
      ))}
    </div>
  )
}
components/ui/landing-page.tsx
tsx
"use client"
import React, { useEffect, useRef, useState, useCallback, useMemo } from "react"
import { GlobeCdn } from "@/components/ui/globe"
import { cn } from "@/lib/utils"

interface ScrollGlobeProps {
  sections: { id: string; badge?: string; title: string; subtitle?: string; description: string; align?: 'left' | 'center' | 'right'; features?: { title: string; description: string }[]; actions?: { label: string; variant: 'primary' | 'secondary'; onClick?: () => void }[] }[]
  globeConfig?: { positions: { top: string; left: string; scale: number }[] }
  className?: string
}

const defaultGlobeConfig = {
  positions: [
    { top: "50%", left: "75%", scale: 1.4 },
    { top: "25%", left: "50%", scale: 0.9 },
    { top: "15%", left: "90%", scale: 2 },
    { top: "50%", left: "50%", scale: 1.8 }
  ]
}

function ScrollGlobe({ sections, globeConfig = defaultGlobeConfig, className }: ScrollGlobeProps) {
  const [activeSection, setActiveSection] = useState(0)
  const [scrollProgress, setScrollProgress] = useState(0)
  const [globeTransform, setGlobeTransform] = useState("")
  const containerRef = useRef<HTMLDivElement>(null)
  const sectionRefs = useRef<(HTMLDivElement | null)[]>([])
  const animationFrameId = useRef<number>()

  const calculatedPositions = useMemo(() => globeConfig.positions.map(pos => ({
    top: parseFloat(pos.top), left: parseFloat(pos.left), scale: pos.scale
  })), [globeConfig.positions])

  const updateScrollPosition = useCallback(() => {
    const scrollTop = window.pageYOffset
    const docHeight = document.documentElement.scrollHeight - window.innerHeight
    const progress = Math.min(Math.max(scrollTop / docHeight, 0), 1)
    setScrollProgress(progress)

    const viewportCenter = window.innerHeight / 2
    let newActive = 0, minDist = Infinity
    sectionRefs.current.forEach((ref, idx) => {
      if (ref) {
        const rect = ref.getBoundingClientRect()
        const dist = Math.abs(rect.top + rect.height / 2 - viewportCenter)
        if (dist < minDist) { minDist = dist; newActive = idx }
      }
    })
    setActiveSection(newActive)
    const pos = calculatedPositions[newActive]
    setGlobeTransform(`translate3d(${pos.left}vw, ${pos.top}vh, 0) translate3d(-50%, -50%, 0) scale3d(${pos.scale}, ${pos.scale}, 1)`)
  }, [calculatedPositions])

  useEffect(() => {
    let ticking = false
    const handleScroll = () => {
      if (!ticking) {
        animationFrameId.current = requestAnimationFrame(() => { updateScrollPosition(); ticking = false })
        ticking = true
      }
    }
    window.addEventListener("scroll", handleScroll, { passive: true })
    updateScrollPosition()
    return () => { window.removeEventListener("scroll", handleScroll); if (animationFrameId.current) cancelAnimationFrame(animationFrameId.current) }
  }, [updateScrollPosition])

  useEffect(() => {
    const pos = calculatedPositions[0]
    setGlobeTransform(`translate3d(${pos.left}vw, ${pos.top}vh, 0) translate3d(-50%, -50%, 0) scale3d(${pos.scale}, ${pos.scale}, 1)`)
  }, [calculatedPositions])

  return (
    <div ref={containerRef} className={cn("relative w-full max-w-screen overflow-x-hidden min-h-screen bg-background text-foreground", className)}>
      {/* Progress Bar */}
      <div className="fixed top-0 left-0 w-full h-0.5 bg-gradient-to-r from-border/20 via-border/40 to-border/20 z-50">
        <div className="h-full bg-gradient-to-r from-primary via-blue-600 to-blue-900 will-change-transform shadow-sm" style={{ transform: `scaleX(${scrollProgress})`, transformOrigin: 'left center', transition: 'transform 0.15s ease-out' }} />
      </div>
      {/* Nav Dots */}
      <div className="hidden sm:flex fixed right-4 lg:right-8 top-1/2 -translate-y-1/2 z-40">
        <div className="space-y-4 lg:space-y-6">
          {sections.map((section, index) => (
            <div key={index} className="relative group">
              <div className={cn("nav-label absolute right-6 lg:right-8 top-1/2 -translate-y-1/2 px-3 lg:px-4 py-1.5 lg:py-2 rounded-lg text-xs sm:text-sm font-medium whitespace-nowrap bg-background/95 backdrop-blur-md border border-border/60 shadow-xl z-50", activeSection === index ? "animate-fadeOut" : "opacity-0")}>
                <div className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-primary animate-pulse" /><span>{section.badge || `Section ${index + 1}`}</span></div>
              </div>
              <button onClick={() => sectionRefs.current[index]?.scrollIntoView({ behavior: 'smooth', block: 'center' })} className={cn("relative w-3 h-3 rounded-full border-2 transition-all duration-300 hover:scale-125 before:absolute before:inset-0 before:rounded-full before:transition-all before:duration-300", activeSection === index ? "bg-primary border-primary shadow-lg before:animate-ping before:bg-primary/20" : "bg-transparent border-muted-foreground/40 hover:border-primary/60 hover:bg-primary/10")} aria-label={`Go to ${section.badge || `section ${index + 1}`}`} />
            </div>
          ))}
        </div>
        <div className="absolute left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-primary/20 to-transparent -translate-x-1/2 -z-10" />
      </div>
      {/* Globe */}
      <div className="fixed z-10 pointer-events-auto will-change-transform transition-all duration-[1400ms] ease-[cubic-bezier(0.23,1,0.32,1)]" style={{ transform: globeTransform, filter: `opacity(${activeSection === 3 ? 0.4 : 0.85})` }}>
        <div className="scale-75 sm:scale-90 lg:scale-100"><GlobeCdn /></div>
      </div>
      {/* Sections */}
      {sections.map((section, index) => (
        <section key={section.id} ref={el => sectionRefs.current[index] = el} className={cn("relative min-h-screen flex flex-col justify-center px-6 lg:px-12 z-20 py-16 lg:py-20 w-full max-w-full overflow-hidden", section.align === 'center' && "items-center text-center", section.align === 'right' && "items-end text-right", (!section.align || section.align === 'left') && "items-start text-left")}>
          <div className={cn("w-full max-w-2xl lg:max-w-4xl will-change-transform transition-all duration-700 opacity-100 translate-y-0")}>
            <h1 className={cn("font-bold mb-6 sm:mb-8 leading-[1.1] tracking-tight", index === 0 ? "text-4xl md:text-5xl lg:text-6xl xl:text-7xl" : "text-3xl md:text-4xl lg:text-5xl xl:text-6xl")}>
              {section.subtitle ? (<div className="space-y-2"><div className="bg-gradient-to-r from-foreground to-foreground/80 bg-clip-text text-transparent">{section.title}</div><div className="text-muted-foreground/90 text-[0.6em] font-medium tracking-wider">{section.subtitle}</div></div>) : (<div className="bg-gradient-to-r from-foreground via-foreground to-foreground/80 bg-clip-text text-transparent">{section.title}</div>)}
            </h1>
            <div className={cn("text-muted-foreground/80 leading-relaxed mb-8 sm:mb-10 text-base lg:text-xl font-light", section.align === 'center' && "max-w-full mx-auto text-center")}>
              <p className="mb-4">{section.description}</p>
              {index === 0 && (
                <div className="flex flex-wrap items-center gap-4 text-xs sm:text-sm text-muted-foreground/60 mt-6">
                  <div className="flex items-center gap-2"><div className="w-1 h-1 rounded-full bg-primary animate-pulse" /><span>Interactive Experience</span></div>
                  <div className="flex items-center gap-2"><div className="w-1 h-1 rounded-full bg-primary animate-pulse" style={{ animationDelay: '0.5s' }} /><span>Scroll to Explore</span></div>
                </div>
              )}
            </div>
            {section.features && (
              <div className="grid gap-4 mb-8 sm:mb-10">
                {section.features.map((feature, i) => (
                  <div key={feature.title} className="group p-5 lg:p-6 rounded-xl border bg-card/50 backdrop-blur-sm hover:bg-card/80 transition-all duration-300 hover:shadow-lg hover:shadow-primary/5 hover:border-primary/20 hover:-translate-y-1">
                    <div className="flex items-start gap-4">
                      <div className="w-2 h-2 rounded-full bg-primary/60 mt-2 group-hover:bg-primary transition-colors flex-shrink-0" />
                      <div className="flex-1 space-y-2">
                        <h3 className="font-semibold text-card-foreground text-lg">{feature.title}</h3>
                        <p className="text-muted-foreground/80 leading-relaxed text-sm lg:text-base">{feature.description}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
            {section.actions && (
              <div className={cn("flex flex-col sm:flex-row flex-wrap gap-4", section.align === 'center' && "justify-center", section.align === 'right' && "justify-end")}>
                {section.actions.map((action, i) => (
                  <button key={action.label} onClick={action.onClick} className={cn("group relative px-6 sm:px-8 py-3 sm:py-4 rounded-xl font-medium transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] text-sm lg:text-base hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-primary/20 w-full sm:w-auto", action.variant === 'primary' ? "bg-primary text-primary-foreground hover:bg-primary/90 shadow-lg shadow-primary/20 hover:shadow-primary/30" : "border-2 border-border/60 bg-background/50 backdrop-blur-sm hover:bg-accent/50 hover:border-primary/30 text-foreground")}>
                    <span className="relative z-10">{action.label}</span>
                    {action.variant === 'primary' && <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-primary to-primary/80 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />}
                  </button>
                ))}
              </div>
            )}
          </div>
        </section>
      ))}
    </div>
  )
}

export default function GlobeScrollDemo() {
  const demoSections = [
    { id: "hero", badge: "Welcome", title: "Explore", subtitle: "Our World", description: "Journey through an immersive experience where technology meets innovation. Watch as perspectives shift and possibilities unfold with every interaction.", align: "left" as const, actions: [{ label: "Begin Journey", variant: "primary" as const }, { label: "Learn More", variant: "secondary" as const }] },
    { id: "innovation", badge: "Innovation", title: "Connected Worldwide", description: "From every corner of the globe, we witness the interconnected web of human achievement. Each connection represents progress.", align: "center" as const },
    { id: "discovery", badge: "Discovery", title: "Expanding", subtitle: "Possibilities", description: "As we push beyond familiar boundaries, new worlds of opportunity emerge. What seemed impossible yesterday becomes tomorrow's foundation.", align: "left" as const, features: [{ title: "Limitless Exploration", description: "Discover new dimensions of possibility and innovation" }, { title: "Seamless Integration", description: "Where cutting-edge technology meets human intuition" }, { title: "Future-Ready Solutions", description: "Built for tomorrow's challenges and opportunities" }] },
    { id: "future", badge: "Future", title: "Our Shared", subtitle: "Tomorrow", description: "In this moment of unity, we see not just a planet, but a canvas of infinite human potential. Every connection represents hope.", align: "center" as const, actions: [{ label: "Join the Movement", variant: "primary" as const }, { label: "Explore More", variant: "secondary" as const }] }
  ]
  return <ScrollGlobe sections={demoSections} className="bg-gradient-to-br from-background via-muted/20 to-background" />
}
components/background-stripes.tsx
tsx
import { cn } from "@/lib/utils"
export function BackgroundStripes({ className }: { className?: string }) {
  return (
    <div className={cn("min-h-screen w-full fixed inset-0 bg-background", className)}>
      <div className="absolute inset-0 z-0" style={{ backgroundImage: `linear-gradient(to right, hsl(var(--border)) 1px, transparent 1px), linear-gradient(to bottom, hsl(var(--border)) 1px, transparent 1px)`, backgroundSize: "40px 40px" }} />
      <div className="absolute inset-0 z-0" style={{ backgroundImage: `radial-gradient(circle at center, rgba(255,249,145,0.15) 0%, transparent 70%)`, mixBlendMode: "multiply" }} />
    </div>
  )
}
components/particle-canvas.tsx
tsx
"use client"
import { useEffect, useRef, useState } from 'react'

const Helper = {
  createShader: (gl: WebGLRenderingContext, type: number, source: string) => { const s = gl.createShader(type)!; gl.shaderSource(s, source); gl.compileShader(s); return s },
  createProgram: (gl: WebGLRenderingContext, vs: WebGLShader, fs: WebGLShader) => { const p = gl.createProgram()!; gl.attachShader(p, vs); gl.attachShader(p, fs); gl.linkProgram(p); return p },
  pixel2DVertexVaryingShader: `attribute vec2 a_position; uniform vec2 u_resolution; attribute vec2 a_color; varying vec2 v_color; void main(){ gl_Position = vec4( vec2( 1, -1 ) * ( ( a_position / u_resolution ) * 2.0 - 1.0 ), 0, 1 ); v_color = a_color; }`,
  uniform2DFragmentVaryingShader: `precision mediump float; varying vec2 v_color; uniform float u_tick; float frac = 1.0/6.0; void main(){ float hue = v_color.x + u_tick; hue = abs(hue - floor(hue)); vec4 color = vec4(0,0,0,1); if(hue<frac){ color.r=1.0; color.g=hue/frac; color.b=0.0; } else if(hue<frac*2.0){ color.r=1.0-(hue-frac)/frac; color.g=1.0; color.b=0.0; } else if(hue<frac*3.0){ color.r=0.0; color.g=1.0; color.b=(hue-frac*2.0)/frac; } else if(hue<frac*4.0){ color.r=0.0; color.g=1.0-(hue-frac*3.0)/frac; color.b=1.0; } else if(hue<frac*5.0){ color.r=(hue-frac*4.0)/frac; color.g=0.0; color.b=1.0; } else { color.r=1.0; color.g=0.0; color.b=1.0-(hue-frac*5.0)/frac; } color=vec4(color.rgb*v_color.y,1.0); gl_FragColor=color; }`
}

export function ParticleCanvas({ maxParticles = 1000, particleSizeMin = 2, particleSizeMax = 5, speedScale = 2 }: { maxParticles?: number; particleSizeMin?: number; particleSizeMax?: number; speedScale?: number }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const webglRef = useRef<any>({})
  const particlesRef = useRef<any[]>([])
  const tickRef = useRef(0)
  const dimensionsRef = useRef({ width: 0, height: 0, cx: 0, cy: 0 })
  const [isAnimating] = useState(true)
  const animationFrameIdRef = useRef<number>()

  function getCircleTriangles(x: number, y: number, r: number) {
    const triangles: number[] = []
    const inc = Math.PI * 2 / 6
    let px = x + r, py = y
    for (let i = 0; i <= Math.PI * 2 + inc; i += inc) {
      const nx = x + r * Math.cos(i), ny = y + r * Math.sin(i)
      triangles.push(x, y, px, py, nx, ny)
      px = nx; py = ny
    }
    return triangles
  }

  function Particle() {
    this.reset = () => {
      this.size = particleSizeMin + (particleSizeMax - particleSizeMin) * Math.random()
      this.x = dimensionsRef.current.cx; this.y = dimensionsRef.current.cy
      this.vx = (Math.random() - 0.5) * 2 * speedScale
      this.vy = -2 - speedScale * Math.random()
      this.time = 1
    }
    this.step = () => {
      this.x += (this.vx *= 0.995); this.y += (this.vy += 0.05); this.time *= 0.99
      const tris = getCircleTriangles(this.x, this.y, this.size * this.time)
      const hue = this.vy / 10
      for (let i = 0; i < tris.length; i += 2) {
        webglRef.current.data.triangles.push(tris[i], tris[i + 1])
        webglRef.current.data.colors.push(hue, this.time)
      }
      if (this.y - this.size > dimensionsRef.current.height) this.reset()
    }
    this.reset()
  }

  useEffect(() => {
    const canvas = canvasRef.current!
    const gl = canvas.getContext('webgl', { alpha: true })!
    const w = window.innerWidth, h = window.innerHeight
    canvas.width = w; canvas.height = h
    dimensionsRef.current = { width: w, height: h, cx: w/2, cy: h/2 }

    webglRef.current.shaderProgram = Helper.createProgram(gl, Helper.createShader(gl, gl.VERTEX_SHADER, Helper.pixel2DVertexVaryingShader), Helper.createShader(gl, gl.FRAGMENT_SHADER, Helper.uniform2DFragmentVaryingShader))
    webglRef.current.attribLocs = {
      position: gl.getAttribLocation(webglRef.current.shaderProgram, 'a_position'),
      color: gl.getAttribLocation(webglRef.current.shaderProgram, 'a_color')
    }
    webglRef.current.buffers = { position: gl.createBuffer(), color: gl.createBuffer() }
    webglRef.current.uniformLocs = {
      resolution: gl.getUniformLocation(webglRef.current.shaderProgram, 'u_resolution'),
      tick: gl.getUniformLocation(webglRef.current.shaderProgram, 'u_tick')
    }
    webglRef.current.data = { triangles: [] as number[], colors: [] as number[] }

    gl.viewport(0, 0, w, h); gl.useProgram(webglRef.current.shaderProgram)
    gl.enableVertexAttribArray(webglRef.current.attribLocs.position)
    gl.enableVertexAttribArray(webglRef.current.attribLocs.color)
    gl.bindBuffer(gl.ARRAY_BUFFER, webglRef.current.buffers.position)
    gl.vertexAttribPointer(webglRef.current.attribLocs.position, 2, gl.FLOAT, false, 0, 0)
    gl.bindBuffer(gl.ARRAY_BUFFER, webglRef.current.buffers.color)
    gl.vertexAttribPointer(webglRef.current.attribLocs.color, 2, gl.FLOAT, false, 0, 0)
    gl.uniform2f(webglRef.current.uniformLocs.resolution, w, h)
    gl.clearColor(0, 0, 0, 0)

    webglRef.current.clear = () => { gl.clear(gl.COLOR_BUFFER_BIT); webglRef.current.data.triangles = []; webglRef.current.data.colors = [] }
    webglRef.current.draw = () => {
      gl.bindBuffer(gl.ARRAY_BUFFER, webglRef.current.buffers.position)
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(webglRef.current.data.triangles), gl.STATIC_DRAW)
      gl.bindBuffer(gl.ARRAY_BUFFER, webglRef.current.buffers.color)
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(webglRef.current.data.colors), gl.STATIC_DRAW)
      gl.drawArrays(gl.TRIANGLES, 0, webglRef.current.data.triangles.length / 2)
    }

    const animate = () => {
      if (!isAnimating) return
      webglRef.current.clear(); tickRef.current++
      if (particlesRef.current.length < maxParticles) particlesRef.current.push(new (Particle as any)(), new (Particle as any)())
      particlesRef.current.sort((a: any, b: any) => a.time - b.time)
      particlesRef.current.forEach((p: any) => p.step())
      gl.uniform1f(webglRef.current.uniformLocs.tick, tickRef.current / 100)
      webglRef.current.draw()
      animationFrameIdRef.current = requestAnimationFrame(animate)
    }
    animationFrameIdRef.current = requestAnimationFrame(animate)

    const handleMouseMove = (e: MouseEvent) => { dimensionsRef.current.cx = e.clientX; dimensionsRef.current.cy = e.clientY }
    const handleResize = () => {
      const w = window.innerWidth, h = window.innerHeight
      canvas.width = w; canvas.height = h
      dimensionsRef.current.width = w; dimensionsRef.current.height = h
      gl.viewport(0, 0, w, h); gl.uniform2f(webglRef.current.uniformLocs.resolution, w, h)
    }
    window.addEventListener('mousemove', handleMouseMove)
    window.addEventListener('resize', handleResize)

    return () => {
      cancelAnimationFrame(animationFrameIdRef.current!)
      window.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('resize', handleResize)
    }
  }, [isAnimating, maxParticles, particleSizeMin, particleSizeMax, speedScale])

  return <canvas ref={canvasRef} style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none" }} />
}
app/globals.css
css
@import "tailwindcss";
@import "tw-animate-css";

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --muted: 0 0% 96.1%;
    --muted-foreground: 0 0% 45.1%;
    --border: 0 0% 89.8%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
  }
  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    --muted: 0 0% 14.9%;
    --muted-foreground: 0 0% 63.9%;
    --border: 0 0% 14.9%;
    --primary: 0 0% 98%;
    --primary-foreground: 0 0% 9%;
  }
}

@keyframes fadeOutLabel {
  0%, 70% { opacity: 1; transform: translateX(0) scale(1); }
  100% { opacity: 0; transform: translateX(0.5rem) scale(0.95); }
}
app/layout.tsx
tsx
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "Global Innovation - Interactive Landing",
  description: "Scroll‑driven storytelling with an interactive 3D globe"
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} bg-background text-foreground`}>{children}</body>
    </html>
  )
}
app/page.tsx
tsx
"use client"
import GlobeScrollDemo from "@/components/ui/landing-page"
import { BackgroundStripes } from "@/components/background-stripes"
import { ParticleCanvas } from "@/components/particle-canvas"

export default function Home() {
  return (
    <>
      <BackgroundStripes />
      <ParticleCanvas maxParticles={5000} />
      <GlobeScrollDemo />
    </>
  )
}