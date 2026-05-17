md
# Add all this

## Setup

```bash
git clone git@github.com:christophacham/agent-skills-library.git
gh repo clone nextlevelbuilder/ui-ux-pro-max-skill
npm install framer-motion
FOR CREATIVE-WHITE – USE THIS GLOBE CODE & IT FINALLY HIGHLIGHT INDIA IN SAFRON WHITE & GREEN THEN SHOW WEBSITE = CODE
components/ui/globe-cdn.tsx

tsx
"use client"

import { useEffect, useRef, useCallback, useState } from "react"
import createGlobe from "cobe"

interface CdnMarker {
  id: string
  location: [number, number]
  region: string
}

interface CdnArc {
  id: string
  from: [number, number]
  to: [number, number]
}

interface GlobeCdnProps {
  markers?: CdnMarker[]
  arcs?: CdnArc[]
  className?: string
  speed?: number
}

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
  { id: "cdn-bom", location: [19.09, 72.87], region: "bom1" },
]

const defaultArcs: CdnArc[] = [
  { id: "cdn-arc-1", from: [38.95, -77.45], to: [49.01, 2.55] },
  { id: "cdn-arc-2", from: [37.62, -122.38], to: [35.55, 139.78] },
  { id: "cdn-arc-3", from: [49.01, 2.55], to: [1.36, 103.99] },
  { id: "cdn-arc-4", from: [38.95, -77.45], to: [-23.43, -46.47] },
  { id: "cdn-arc-5", from: [35.55, 139.78], to: [-33.95, 151.18] },
  { id: "cdn-arc-6", from: [49.01, 2.55], to: [19.09, 72.87] },
]

export function GlobeCdn({
  markers = defaultMarkers,
  arcs = defaultArcs,
  className = "",
  speed = 0.003,
}: GlobeCdnProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const pointerInteracting = useRef<{ x: number; y: number } | null>(null)
  const dragOffset = useRef({ phi: 0, theta: 0 })
  const phiOffsetRef = useRef(0)
  const thetaOffsetRef = useRef(0)
  const isPausedRef = useRef(false)
  const [traffic, setTraffic] = useState(() =>
    defaultArcs.map((a, i) => ({ id: a.id, value: [420, 380, 290, 185, 156, 134][i] || 100 }))
  )

  useEffect(() => {
    const interval = setInterval(() => {
      setTraffic((data) =>
        data.map((t) => ({
          ...t,
          value: Math.max(50, t.value + Math.floor(Math.random() * 21) - 10),
        }))
      )
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
          theta: (e.clientY - pointerInteracting.current.y) / 1000,
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
      markers: markers.map((m) => ({ location: m.location, size: 0.012, id: m.id })),
      arcs: arcs.map((a) => ({ from: a.from, to: a.to, id: a.id })),
      arcColor: [0, 0, 0],
      arcWidth: 0.5, arcHeight: 0.25, opacity: 0.7,
    })
    function animate() {
      if (!isPausedRef.current) phi += speed
      globe!.update({
        phi: phi + phiOffsetRef.current + dragOffset.current.phi,
        theta: 0.2 + thetaOffsetRef.current + dragOffset.current.theta,
      })
      animationId = requestAnimationFrame(animate)
    }
      animate()
      setTimeout(() => canvas && (canvas.style.opacity = "1"))
    }

    if (canvas.offsetWidth > 0) {
      init()
    } else {
      const ro = new ResizeObserver((entries) => {
        if (entries[0]?.contentRect.width > 0) {
          ro.disconnect()
          init()
        }
      })
      ro.observe(canvas)
    }

    return () => {
      if (animationId) cancelAnimationFrame(animationId)
      if (globe) globe.destroy()
    }
  }, [markers, arcs, speed])

  const pyramidFaceStyle = (nth: number): React.CSSProperties => {
    const transforms = [
      "rotateY(0deg) translateZ(4px) rotateX(19.5deg)",
      "rotateY(120deg) translateZ(4px) rotateX(19.5deg)",
      "rotateY(240deg) translateZ(4px) rotateX(19.5deg)",
      "rotateX(-90deg) rotateZ(60deg) translateY(4px)",
    ]
    const colors = ["#111", "#333", "#555", "#222"]
    return {
      position: "absolute", left: -0.5, top: 0,
      width: 0, height: 0,
      borderLeft: "6.5px solid transparent",
      borderRight: "6.5px solid transparent",
      borderBottom: `13px solid ${colors[nth]}`,
      transformOrigin: "center bottom",
      transform: transforms[nth],
    }
  }

  return (
    <div className={`relative aspect-square select-none ${className}`}>
      <style>{`
        @keyframes pyramid-spin {
          0% { transform: rotateX(20deg) rotateY(0deg); }
          100% { transform: rotateX(20deg) rotateY(360deg); }
        }
      `}</style>
      <canvas
        ref={canvasRef}
        onPointerDown={handlePointerDown}
        style={{
          width: "100%", height: "100%", cursor: "grab", opacity: 0,
          transition: "opacity 1.2s ease", borderRadius: "50%", touchAction: "none",
        }}
      />
      {markers.map((m) => (
        <div
          key={m.id}
          style={{
            position: "absolute",
            // @ts-expect-error CSS Anchor Positioning
            positionAnchor: `--cobe-${m.id}`,
            bottom: "anchor(top)",
            left: "anchor(center)",
            translate: "-50% 0",
            display: "flex",
            flexDirection: "column" as const,
            alignItems: "center",
            gap: 6,
            pointerEvents: "none" as const,
            opacity: `var(--cobe-visible-${m.id}, 0)`,
            filter: `blur(calc((1 - var(--cobe-visible-${m.id}, 0)) * 8px))`,
            transition: "opacity 0.3s, filter 0.3s",
          }}
        >
          <div style={{
            width: 12, height: 12, position: "relative",
            transformStyle: "preserve-3d" as const,
            animation: "pyramid-spin 4s linear infinite",
          }}>
            {[0, 1, 2, 3].map((n) => (
              <div key={n} style={pyramidFaceStyle(n)} />
            ))}
          </div>
          <span style={{
            fontFamily: "monospace", fontSize: "0.55rem", color: "#000",
            background: "#fff", padding: "2px 6px", borderRadius: 3,
            letterSpacing: "0.05em", whiteSpace: "nowrap" as const,
            boxShadow: "0 1px 3px rgba(0,0,0,0.2)",
          }}>{m.region}</span>
        </div>
      ))}
      {traffic.map((t) => (
        <div
          key={t.id}
          style={{
            position: "absolute",
            // @ts-expect-error CSS Anchor Positioning
            positionAnchor: `--cobe-arc-${t.id}`,
            bottom: "anchor(top)",
            left: "anchor(center)",
            translate: "-50% 0",
            fontFamily: "monospace",
            fontSize: "0.5rem",
            color: "#fff",
            background: "#000",
            padding: "3px 8px",
            borderRadius: 4,
            whiteSpace: "nowrap" as const,
            pointerEvents: "none" as const,
            opacity: `var(--cobe-visible-arc-${t.id}, 0)`,
            filter: `blur(calc((1 - var(--cobe-visible-arc-${t.id}, 0)) * 8px))`,
            transition: "opacity 0.3s, filter 0.3s",
          }}
        >
          {t.value}k req/s
        </div>
      ))}
    </div>
  )
}
SO THIS EARTH MOVE IT HOW ITS MENTIONED IN THIS PROMPT !!
components/ui/landing-page.tsx

tsx
import React, { useEffect, useRef, useState, useCallback, useMemo } from "react"; 
import Globe from "@/components/ui/globe";
import { cn } from "@/lib/utils";

// Reusable ScrollGlobe component following shadcn/ui patterns
interface ScrollGlobeProps {
  sections: {
    id: string;
    badge?: string;
    title: string;
    subtitle?: string;
    description: string;
    align?: 'left' | 'center' | 'right';
    features?: { title: string; description: string }[];
    actions?: { label: string; variant: 'primary' | 'secondary'; onClick?: () => void }[];
  }[];
  globeConfig?: {
    positions: {
      top: string;
      left: string;
      scale: number;
    }[];
  };
  className?: string;
}

const defaultGlobeConfig = {
  positions: [
    { top: "50%", left: "75%", scale: 1.4 },  // Hero: Right side, balanced
    { top: "25%", left: "50%", scale: 0.9 },  // Innovation: Top side, subtle
    { top: "15%", left: "90%", scale: 2 },  // Discovery: Left side, medium
    { top: "50%", left: "50%", scale: 1.8 },  // Future: Center, large backdrop
  ]
};

// Utility function to smoothly interpolate between values
const lerp = (start: number, end: number, factor: number): number => {
  return start + (end - start) * factor;
};

// Parse percentage string to number
const parsePercent = (str: string): number => parseFloat(str.replace('%', ''));

function ScrollGlobe({ sections, globeConfig = defaultGlobeConfig, className }: ScrollGlobeProps) {
  const [activeSection, setActiveSection] = useState(0);
  const [scrollProgress, setScrollProgress] = useState(0);
  const [globeTransform, setGlobeTransform] = useState("");
  const [showNavLabel, setShowNavLabel] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const sectionRefs = useRef<(HTMLDivElement | null)[]>([]);
  const lastScrollTime = useRef(0);
  const animationFrameId = useRef<number>();
  const navLabelTimeoutRef = useRef<NodeJS.Timeout>();
  
  // Pre-calculate positions for performance
  const calculatedPositions = useMemo(() => {
    return globeConfig.positions.map(pos => ({
      top: parsePercent(pos.top),
      left: parsePercent(pos.left),
      scale: pos.scale
    }));
  }, [globeConfig.positions]);

  // Simple, direct scroll tracking
  const updateScrollPosition = useCallback(() => {
    const scrollTop = window.pageYOffset;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = Math.min(Math.max(scrollTop / docHeight, 0), 1);
    
    setScrollProgress(progress);

    // Simple section detection
    const viewportCenter = window.innerHeight / 2;
    let newActiveSection = 0;
    let minDistance = Infinity;

    sectionRefs.current.forEach((ref, index) => {
      if (ref) {
        const rect = ref.getBoundingClientRect();
        const sectionCenter = rect.top + rect.height / 2;
        const distance = Math.abs(sectionCenter - viewportCenter);
        
        if (distance < minDistance) {
          minDistance = distance;
          newActiveSection = index;
        }
      }
    });

    // Direct position update - no interpolation
    const currentPos = calculatedPositions[newActiveSection];
    const transform = `translate3d(${currentPos.left}vw, ${currentPos.top}vh, 0) translate3d(-50%, -50%, 0) scale3d(${currentPos.scale}, ${currentPos.scale}, 1)`;
    
    setGlobeTransform(transform);

    setActiveSection(newActiveSection);
  }, [calculatedPositions, activeSection]);

  // Throttled scroll handler with RAF
  useEffect(() => {
    let ticking = false;
    
    const handleScroll = () => {
      if (!ticking) {
        animationFrameId.current = requestAnimationFrame(() => {
          updateScrollPosition();
          ticking = false;
        });
        ticking = true;
      }
    };

    // Use passive listeners and immediate execution
    window.addEventListener("scroll", handleScroll, { passive: true });
    updateScrollPosition(); // Initial call
    
    return () => {
      window.removeEventListener("scroll", handleScroll);
      if (animationFrameId.current) {
        cancelAnimationFrame(animationFrameId.current);
      }
      if (navLabelTimeoutRef.current) {
        clearTimeout(navLabelTimeoutRef.current);
      }
    };
  }, [updateScrollPosition]);

  // Initial globe position
  useEffect(() => {
    const initialPos = calculatedPositions[0];
    const initialTransform = `translate3d(${initialPos.left}vw, ${initialPos.top}vh, 0) translate3d(-50%, -50%, 0) scale3d(${initialPos.scale}, ${initialPos.scale}, 1)`;
    setGlobeTransform(initialTransform);
  }, [calculatedPositions]);

  return (
    <div 
      ref={containerRef}
      className={cn(
        "relative w-full max-w-screen overflow-x-hidden min-h-screen bg-background text-foreground",
        className
      )}
    >
      {/* Progress Bar */}
      <div className="fixed top-0 left-0 w-full h-0.5 bg-gradient-to-r from-border/20 via-border/40 to-border/20 z-50">
        <div 
          className="h-full bg-gradient-to-r from-primary via-blue-600 to-blue-900 will-change-transform shadow-sm"
          style={{ 
            transform: `scaleX(${scrollProgress})`,
            transformOrigin: 'left center',
            transition: 'transform 0.15s ease-out',
            filter: 'drop-shadow(0 0 2px rgba(59, 130, 246, 0.3))'
          }}
        />
      </div>

      {/* Enhanced Navigation with auto-hiding labels - Fully Responsive */}
      <div className="hidden sm:flex fixed right-2 sm:right-4 lg:right-8 top-1/2 -translate-y-1/2 z-40">
        <div className="space-y-3 sm:space-y-4 lg:space-y-6">
          {sections.map((section, index) => (
            <div key={index} className="relative group">
              {/* Auto-hiding section label - Always visible but with responsive sizing */}
              <div
                className={cn(
                  "nav-label absolute right-5 sm:right-6 lg:right-8 top-1/2 -translate-y-1/2",
                  "px-2 sm:px-3 lg:px-4 py-1 sm:py-1.5 lg:py-2 rounded-md sm:rounded-lg text-xs sm:text-sm font-medium whitespace-nowrap",
                  "bg-background/95 backdrop-blur-md border border-border/60 shadow-xl z-50",
                  activeSection === index ? "animate-fadeOut" : "opacity-0"
                )}
              >
                <div className="flex items-center gap-1 sm:gap-1.5 lg:gap-2">
                  <div className="w-1 sm:w-1.5 lg:w-2 h-1 sm:h-1.5 lg:h-2 rounded-full bg-primary animate-pulse" />
                  <span className="text-xs sm:text-sm lg:text-base">
                    {section.badge || `Section ${index + 1}`}
                  </span>
                </div>
              </div>

              <button
                onClick={() => {
                  sectionRefs.current[index]?.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'center'
                  });
                }}
                className={cn(
                  "relative w-2 h-2 sm:w-2.5 sm:h-2.5 lg:w-3 lg:h-3 rounded-full border-2 transition-all duration-300 hover:scale-125",
                  "before:absolute before:inset-0 before:rounded-full before:transition-all before:duration-300",
                  activeSection === index 
                    ? "bg-primary border-primary shadow-lg before:animate-ping before:bg-primary/20" 
                    : "bg-transparent border-muted-foreground/40 hover:border-primary/60 hover:bg-primary/10"
                )}
                aria-label={`Go to ${section.badge || `section ${index + 1}`}`}
              />
            </div>
          ))}
        </div>
        
        {/* Enhanced navigation line - Responsive */}
        <div className="absolute left-1/2 top-0 bottom-0 w-0.5 lg:w-px bg-gradient-to-b from-transparent via-primary/20 to-transparent -translate-x-1/2 -z-10" />
      </div>

      {/* Ultra-smooth Globe with responsive scaling */}
      <div
        className="fixed z-10 pointer-events-none will-change-transform transition-all duration-[1400ms] ease-[cubic-bezier(0.23,1,0.32,1)]"
        style={{
          transform: globeTransform,
          filter: `opacity(${activeSection === 3 ? 0.4 : 0.85})`, // Subtle opacity for backdrop effect
        }}
      >
        <div className="scale-75 sm:scale-90 lg:scale-100">
          <Globe />
        </div>
      </div>

      {/* Dynamic sections - fully responsive */}
      {sections.map((section, index) => (
        <section
          key={section.id}
          ref={(el) => (sectionRefs.current[index] = el)}
          className={cn(
            "relative min-h-screen flex flex-col justify-center px-4 sm:px-6 md:px-8 lg:px-12 z-20 py-12 sm:py-16 lg:py-20",
            "w-full max-w-full overflow-hidden",
            section.align === 'center' && "items-center text-center",
            section.align === 'right' && "items-end text-right",
            section.align !== 'center' && section.align !== 'right' && "items-start text-left"
          )}
        >
          <div className={cn(
            "w-full max-w-sm sm:max-w-lg md:max-w-2xl lg:max-w-4xl xl:max-w-5xl will-change-transform transition-all duration-700",
            "opacity-100 translate-y-0"
          )}>
            
            <h1 className={cn(
              "font-bold mb-6 sm:mb-8 leading-[1.1] tracking-tight",
              index === 0 
                ? "text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl 2xl:text-8xl" 
                : "text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl 2xl:text-7xl"
            )}>
              {section.subtitle ? (
                <div className="space-y-1 sm:space-y-2">
                  <div className="bg-gradient-to-r from-foreground to-foreground/80 bg-clip-text text-transparent">
                    {section.title}
                  </div>
                  <div className="text-muted-foreground/90 text-[0.6em] sm:text-[0.7em] font-medium tracking-wider">
                    {section.subtitle}
                  </div>
                </div>
              ) : (
                <div className="bg-gradient-to-r from-foreground via-foreground to-foreground/80 bg-clip-text text-transparent">
                  {section.title}
                </div>
              )}
            </h1>
            
            <div className={cn(
              "text-muted-foreground/80 leading-relaxed mb-8 sm:mb-10 text-base sm:text-lg lg:text-xl font-light",
              section.align === 'center' ? "max-w-full mx-auto text-center" : "max-w-full"
            )}>
              <p className="mb-3 sm:mb-4">{section.description}</p>
              {index === 0 && (
                <div className="flex flex-wrap items-center gap-3 sm:gap-4 text-xs sm:text-sm text-muted-foreground/60 mt-4 sm:mt-6">
                  <div className="flex items-center gap-1.5 sm:gap-2">
                    <div className="w-1 h-1 rounded-full bg-primary animate-pulse" />
                    <span>Interactive Experience</span>
                  </div>
                  <div className="flex items-center gap-1.5 sm:gap-2">
                    <div className="w-1 h-1 rounded-full bg-primary animate-pulse" style={{ animationDelay: '0.5s' }} />
                    <span>Scroll to Explore</span>
                  </div>
                </div>
              )}
            </div>

            {/* Enhanced Features - Responsive grid */}
            {section.features && (
              <div className="grid gap-3 sm:gap-4 mb-8 sm:mb-10">
                {section.features.map((feature, featureIndex) => (
                  <div 
                    key={feature.title}
                    className={cn(
                      "group p-4 sm:p-5 lg:p-6 rounded-lg sm:rounded-xl border bg-card/50 backdrop-blur-sm hover:bg-card/80 transition-all duration-300 hover:shadow-lg hover:shadow-primary/5",
                      "hover:border-primary/20 hover:-translate-y-1"
                    )}
                    style={{ animationDelay: `${featureIndex * 0.1}s` }}
                  >
                    <div className="flex items-start gap-3 sm:gap-4">
                      <div className="w-1.5 sm:w-2 h-1.5 sm:h-2 rounded-full bg-primary/60 mt-1.5 sm:mt-2 group-hover:bg-primary transition-colors flex-shrink-0" />
                      <div className="flex-1 space-y-1.5 sm:space-y-2 min-w-0">
                        <h3 className="font-semibold text-card-foreground text-base sm:text-lg">{feature.title}</h3>
                        <p className="text-muted-foreground/80 leading-relaxed text-sm sm:text-base">{feature.description}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Enhanced Actions - Responsive buttons */}
            {section.actions && (
              <div className={cn(
                "flex flex-col sm:flex-row flex-wrap gap-3 sm:gap-4",
                section.align === 'center' && "justify-center",
                section.align === 'right' && "justify-end",
                (!section.align || section.align === 'left') && "justify-start"
              )}>
                {section.actions.map((action, actionIndex) => (
                  <button
                    key={action.label}
                    onClick={action.onClick}
                    className={cn(
                      "group relative px-6 sm:px-8 py-3 sm:py-4 rounded-lg sm:rounded-xl font-medium transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] text-sm sm:text-base",
                      "hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-primary/20 w-full sm:w-auto",
                      action.variant === 'primary' 
                        ? "bg-primary text-primary-foreground hover:bg-primary/90 shadow-lg shadow-primary/20 hover:shadow-primary/30" 
                        : "border-2 border-border/60 bg-background/50 backdrop-blur-sm hover:bg-accent/50 hover:border-primary/30 text-foreground"
                    )}
                    style={{ animationDelay: `${actionIndex * 0.1 + 0.2}s` }}
                  >
                    <span className="relative z-10">{action.label}</span>
                    {action.variant === 'primary' && (
                      <div className="absolute inset-0 rounded-lg sm:rounded-xl bg-gradient-to-r from-primary to-primary/80 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    )}
                  </button>
                ))}
              </div>
            )}
          </div>
        </section>
      ))}
    </div>
  );
}

// Demo component showcasing the ScrollGlobe
export default function GlobeScrollDemo() {
  const demoSections = [
    {
      id: "hero",
      badge: "Welcome",
      title: "Explore",
      subtitle: "Our World",
      description: "Journey through an immersive experience where technology meets innovation. Watch as perspectives shift and possibilities unfold with every interaction, creating a symphony of digital artistry.",
      align: "left" as const,
      actions: [
        { label: "Begin Journey", variant: "primary" as const, onClick: () => console.log("Get started clicked") },
        { label: "Learn More", variant: "secondary" as const, onClick: () => console.log("Learn more clicked") },
      ]
    },
    {
      id: "innovation",
      badge: "Innovation",
      title: "Connected Worldwide",
      description: "From every corner of the globe, we witness the interconnected web of human achievement. Each connection represents progress, every interaction drives innovation forward into uncharted territories.",
      align: "center" as const,
    },
    {
      id: "discovery",
      badge: "Discovery",
      title: "Expanding",
      subtitle: "Possibilities",
      description: "As we push beyond familiar boundaries, new worlds of opportunity emerge from the horizon. What seemed impossible yesterday becomes tomorrow's foundation for extraordinary achievements.",
      align: "left" as const,
      features: [
        { title: "Limitless Exploration", description: "Discover new dimensions of possibility and innovation" },
        { title: "Seamless Integration", description: "Where cutting-edge technology meets human intuition" },
        { title: "Future-Ready Solutions", description: "Built for tomorrow's challenges and opportunities" }
      ]
    },
    {
      id: "future",
      badge: "Future",
      title: "Our Shared",
      subtitle: "Tomorrow",
      description: "In this moment of unity, we see not just a planet, but a canvas of infinite human potential. Every connection represents hope, every innovation builds bridges to our collective future of endless possibilities.",
      align: "center" as const,
      actions: [
        { label: "Join the Movement", variant: "primary" as const, onClick: () => console.log("Join clicked") },
        { label: "Explore More", variant: "secondary" as const, onClick: () => console.log("Explore clicked") }
      ]
    }
  ];

  return (
    <ScrollGlobe 
      sections={demoSections}
      className="bg-gradient-to-br from-background via-muted/20 to-background"
    />
  );
}
components/ui/demo.tsx

tsx
import Component from "@/components/ui/landing-page";

export default function DemoOne() {
  return <Component />;
}
components/ui/globe.tsx (the dependency for landing-page)

tsx
import React from "react";

const Globe: React.FC = () => {
  return (
    <>
      <style>
        {`
          @keyframes earthRotate {
            0% { background-position: 0 0; }
            100% { background-position: 400px 0; }
          }
          @keyframes twinkling { 0%,100% { opacity:0.1; } 50% { opacity:1; } }
          @keyframes twinkling-slow { 0%,100% { opacity:0.1; } 50% { opacity:1; } }
          @keyframes twinkling-long { 0%,100% { opacity:0.1; } 50% { opacity:1; } }
          @keyframes twinkling-fast { 0%,100% { opacity:0.1; } 50% { opacity:1; } }
        `}
      </style>
      <div className="flex items-center justify-center h-screen">
        <div
          className="relative w-[250px] h-[250px] rounded-full overflow-hidden shadow-[0_0_20px_rgba(255,255,255,0.2),-5px_0_8px_#c3f4ff_inset,15px_2px_25px_#000_inset,-24px_-2px_34px_#c3f4ff99_inset,250px_0_44px_#00000066_inset,150px_0_38px_#000000aa_inset]"
          style={{
            backgroundImage: "url('https://pub-940ccf6255b54fa799a9b01050e6c227.r2.dev/globe.jpeg')",
            backgroundSize: "cover",
            backgroundPosition: "left",
            animation: "earthRotate 30s linear infinite",
          }}
        >
          {/* Stars */}
          <div
            className="absolute left-[-20px] w-1 h-1 bg-white rounded-full"
            style={{ animation: "twinkling 3s infinite" }}
          />
          <div
            className="absolute left-[-40px] top-[30px] w-1 h-1 bg-white rounded-full"
            style={{ animation: "twinkling-slow 2s infinite" }}
          />
          <div
            className="absolute left-[350px] top-[90px] w-1 h-1 bg-white rounded-full"
            style={{ animation: "twinkling-long 4s infinite" }}
          />
          <div
            className="absolute left-[200px] top-[290px] w-1 h-1 bg-white rounded-full"
            style={{ animation: "twinkling 3s infinite" }}
          />
          <div
            className="absolute left-[50px] top-[270px] w-1 h-1 bg-white rounded-full"
            style={{ animation: "twinkling-fast 1.5s infinite" }}
          />
          <div
            className="absolute left-[250px] top-[-50px] w-1 h-1 bg-white rounded-full"
            style={{ animation: "twinkling-long 4s infinite" }}
          />
          <div
            className="absolute left-[290px] top-[60px] w-1 h-1 bg-white rounded-full"
            style={{ animation: "twinkling-slow 2s infinite" }}
          />
        </div>
      </div>
    </>
  );
};

export default Globe;
Extend existing Tailwind 4 index.css with this code (or if project uses Tailwind 3, extend tailwind.config.js or globals.css):

css
@import "tailwindcss";
@import "tw-animate-css";


@keyframes fadeOutLabel {
  0% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
  70% {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateX(0.5rem) scale(0.95);
  }
}
KEEP THE OVERALL BACKGROUND LIKE THIS STRIPES
components/ui/background-components.tsx

tsx
import { cn } from "@/lib/utils";
import { useState } from "react";

export const Component = () => {
  const [count, setCount] = useState(0);

  return (
   <div className="min-h-screen w-full relative bg-white">
  {/* Soft Yellow Glow */}
  <div
    className="absolute inset-0 z-0"
    style={{
      backgroundImage: `
        radial-gradient(circle at center, #FFF991 0%, transparent 70%)
      `,
      opacity: 0.6,
      mixBlendMode: "multiply",
    }}
  />
     {/* Your Content/Components */}
</div>
  );
};


// demo.tsx
// This is file of your component
// You can use any dependencies from npm; we import them automatically in package.json

import { cn } from "@/lib/utils";
import { useState } from "react";

export const Component = () => {
  const [count, setCount] = useState(0);

  return (
    <div className="min-h-screen w-full bg-white relative">
  {/* Grid Background */}
  <div
    className="absolute inset-0 z-0"
    style={{
      backgroundImage: `
        linear-gradient(to right, #e5e7eb 1px, transparent 1px),
        linear-gradient(to bottom, #e5e7eb 1px, transparent 1px)
      `,
      backgroundSize: "40px 40px",
    }}
  />
     {/* Your Content/Components */}
</div>

  );
};

export default Component;
FOR MOUSE ANIMATION USE THIS CODE
components/ui/particle-canvas.tsx

tsx
import { useEffect, useRef, useState } from 'react';

const Helper = {
  createShader: (gl, type, source) => {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    return shader;
  },
  createProgram: (gl, vertexShader, fragmentShader) => {
    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    return program;
  },
  pixel2DVertexVaryingShader: `
    attribute vec2 a_position;
    uniform vec2 u_resolution;
    attribute vec2 a_color;
    varying vec2 v_color;
    void main(){
      gl_Position = vec4( vec2( 1, -1 ) * ( ( a_position / u_resolution ) * 2.0 - 1.0 ), 0, 1 );
      v_color = a_color;
    }
  `,
  uniform2DFragmentVaryingShader: `
    precision mediump float;
    varying vec2 v_color;
    uniform float u_tick;
    float frac = 1.0/6.0;
    void main(){
      float hue = v_color.x + u_tick;
      hue = abs(hue - floor(hue));
      vec4 color = vec4( 0, 0, 0, 1 );
      if( hue < frac ){
        color.r = 1.0;
        color.g = hue / frac;
        color.b = 0.0;
      } else if( hue < frac * 2.0 ){
        color.r = 1.0 - ( hue - frac ) / frac;
        color.g = 1.0;
        color.b = 0.0;
      } else if( hue < frac * 3.0 ){
        color.r = 0.0;
        color.g = 1.0;
        color.b = ( hue - frac * 2.0 ) / frac;
      } else if( hue < frac * 4.0 ){
        color.r = 0.0;
        color.g = 1.0 - ( hue - frac * 3.0 ) / frac;
        color.b = 1.0;
      } else if( hue < frac * 5.0 ){
        color.r = ( hue - frac * 4.0 ) / frac;
        color.g = 0.0;
        color.b = 1.0;
      } else {
        color.r = 1.0;
        color.g = 0.0;
        color.b = 1.0 - ( hue - frac * 5.0 ) / frac;
      }
      color = vec4( color.rgb * v_color.y, 1.0 );
      gl_FragColor = color;
    }
  `
};

const ParticleCanvas = ({ maxParticles = 1000, particleSizeMin = 2, particleSizeMax = 5, speedScale = 2 }) => {
  const canvasRef = useRef(null);
  const webglRef = useRef({});
  const particlesRef = useRef([]);
  const tickRef = useRef(0);
  const dimensionsRef = useRef({ width: 0, height: 0, cx: 0, cy: 0 });
  const [isAnimating] = useState(true);
  const animationFrameIdRef = useRef(null);

  function getCircleTriangles(x, y, r) {
    const triangles = [];
    const inc = Math.PI * 2 / 6;
    let px = x + r;
    let py = y;
    for (let i = 0; i <= Math.PI * 2 + inc; i += inc) {
      const nx = x + r * Math.cos(i);
      const ny = y + r * Math.sin(i);
      triangles.push(x, y, px, py, nx, ny);
      px = nx;
      py = ny;
    }
    return triangles;
  }

  function Particle() {
    this.reset = () => {
      this.size = particleSizeMin + (particleSizeMax - particleSizeMin) * Math.random();
      this.x = dimensionsRef.current.cx;
      this.y = dimensionsRef.current.cy;
      this.vx = (Math.random() - 0.5) * 2 * speedScale;
      this.vy = -2 - speedScale * Math.random();
      this.time = 1;
    };
    this.step = () => {
      this.x += (this.vx *= 0.995);
      this.y += (this.vy += 0.05);
      this.time *= 0.99;
      const triangles = getCircleTriangles(this.x, this.y, this.size * this.time);
      const hue = this.vy / 10;
      for (let i = 0; i < triangles.length; i += 2) {
        webglRef.current.data.triangles.push(triangles[i], triangles[i + 1]);
        webglRef.current.data.colors.push(hue, this.time);
      }
      if (this.y - this.size > dimensionsRef.current.height) {
        this.reset();
      }
    };
    this.reset();
  }

  useEffect(() => {
    const canvas = canvasRef.current;
    const gl = canvas.getContext('webgl', { alpha: true }); // enable alpha
    if (!gl) return;

    const w = window.innerWidth;
    const h = window.innerHeight;
    canvas.width = w;
    canvas.height = h;
    dimensionsRef.current = { width: w, height: h, cx: w / 2, cy: h / 2 };

    webglRef.current.shaderProgram = Helper.createProgram(
      gl,
      Helper.createShader(gl, gl.VERTEX_SHADER, Helper.pixel2DVertexVaryingShader),
      Helper.createShader(gl, gl.FRAGMENT_SHADER, Helper.uniform2DFragmentVaryingShader)
    );
    webglRef.current.attribLocs = {
      position: gl.getAttribLocation(webglRef.current.shaderProgram, 'a_position'),
      color: gl.getAttribLocation(webglRef.current.shaderProgram, 'a_color')
    };
    webglRef.current.buffers = {
      position: gl.createBuffer(),
      color: gl.createBuffer()
    };
    webglRef.current.uniformLocs = {
      resolution: gl.getUniformLocation(webglRef.current.shaderProgram, 'u_resolution'),
      tick: gl.getUniformLocation(webglRef.current.shaderProgram, 'u_tick')
    };
    webglRef.current.data = { triangles: [], colors: [] };

    gl.viewport(0, 0, w, h);
    gl.useProgram(webglRef.current.shaderProgram);
    gl.enableVertexAttribArray(webglRef.current.attribLocs.position);
    gl.enableVertexAttribArray(webglRef.current.attribLocs.color);
    gl.bindBuffer(gl.ARRAY_BUFFER, webglRef.current.buffers.position);
    gl.vertexAttribPointer(webglRef.current.attribLocs.position, 2, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, webglRef.current.buffers.color);
    gl.vertexAttribPointer(webglRef.current.attribLocs.color, 2, gl.FLOAT, false, 0, 0);
    gl.uniform2f(webglRef.current.uniformLocs.resolution, w, h);

    // transparent clear
    gl.clearColor(0, 0, 0, 0);

    webglRef.current.clear = () => {
      gl.clear(gl.COLOR_BUFFER_BIT);
      webglRef.current.data.triangles = [];
      webglRef.current.data.colors = [];
    };

    webglRef.current.draw = () => {
      gl.bindBuffer(gl.ARRAY_BUFFER, webglRef.current.buffers.position);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(webglRef.current.data.triangles), gl.STATIC_DRAW);
      gl.bindBuffer(gl.ARRAY_BUFFER, webglRef.current.buffers.color);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(webglRef.current.data.colors), gl.STATIC_DRAW);
      gl.drawArrays(gl.TRIANGLES, 0, webglRef.current.data.triangles.length / 2);
    };

    const animate = () => {
      if (!isAnimating) return;
      webglRef.current.clear();
      tickRef.current++;
      if (particlesRef.current.length < maxParticles) {
        particlesRef.current.push(new Particle(), new Particle());
      }
      particlesRef.current.sort((a, b) => a.time - b.time);
      particlesRef.current.forEach(particle => particle.step());
      gl.uniform1f(webglRef.current.uniformLocs.tick, tickRef.current / 100);
      webglRef.current.draw();
      animationFrameIdRef.current = requestAnimationFrame(animate);
    };

    animationFrameIdRef.current = requestAnimationFrame(animate);

    const handleMouseMove = (e) => {
      dimensionsRef.current.cx = e.clientX;
      dimensionsRef.current.cy = e.clientY;
    };

    const handleResize = () => {
      const w = window.innerWidth;
      const h = window.innerHeight;
      canvas.width = w;
      canvas.height = h;
      dimensionsRef.current.width = w;
      dimensionsRef.current.height = h;
      gl.viewport(0, 0, w, h);
      gl.uniform2f(webglRef.current.uniformLocs.resolution, w, h);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrameIdRef.current);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
    };
  }, [isAnimating, maxParticles, particleSizeMin, particleSizeMax, speedScale]);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        pointerEvents: "none", // so it doesn’t block clicks
      }}
    />
  );
};

export { ParticleCanvas };
Implementation Guidelines
Analyze the component structure and identify all required dependencies

Review the component's arguments and state

Identify any required context providers or hooks and install them

Questions to Ask

What data/props will be passed to this component?

Are there any specific state management requirements?

Are there any required assets (images, icons, etc.)?

What is the expected responsive behavior?

What is the best place to use this component in the app?

Steps to integrate
Copy paste all the code above in the correct directories

Install external dependencies

Fill image assets with Unsplash stock images you know exist

Use lucide-react icons for svgs or logos if component requires them

text
U TYPED EXCEEDING 5K LIMIT INPUT 

INStead of full codes give it a little code little let it figure out 

make overalll less than 5 000 char !!
We need to condense the response significantly, under 5000 characters. The user gave a huge prompt with many code files and wants a concise summary in markdown, not the full code. The original request: "DONT GIVE IT HOW TO STRUCTURE THE CODEFILES ... CONCISE INTO ONE MD (CODE + TEXT ) SAME TONE ADD THIS .......... DONT GIVE UR OWN CONTEXT FOR IT JUST SAY ADD ALL THIS". So they want the instructions to add all these files, but without the long full code blocks, just a concise summary of what to copy-paste and where, with small code snippets perhaps, but overall under 5k char. The assistant gave all codes in full, exceeding limit. Now they're saying "U TYPED EXCEEDING 5K LIMIT INPUT INStead of full codes give it a little code little let it figure out make overalll less than 5 000 char !!"

So I need to rewrite the response into a concise markdown file that instructs to add all these files, but without pasting the full code. Instead, I'll provide the file paths and maybe a brief description or a tiny snippet to indicate, and the user can figure out from the context they already have? Wait, the user originally gave the code themselves. They already have the code. They want a summarized instruction md that says "add all this" and lists where to put each file, without the actual full code blocks. But they want to keep the code+text tone, but under 5k char. I think they want me to just list the files and maybe a tiny code snippet that's essential (like the globe cdn or the landing page) but very condensed. They said "give it a little code little let it figure out". So I'll produce a markdown with sections, but only include the most critical minimal code snippets (like the import lines or the custom animations) and for the large components, just say "add the code as provided" with a short note. I need to ensure total characters < 5000.

Let's plan:

Keep the beginning setup commands.

For each component, give file name, and a one-liner of what it is, maybe a small code snippet that shows the key part.

For the background stripes, give a small snippet.

For mouse particle canvas, give a small snippet.

For the globe with India highlight, I'll just say to modify the defaultMarkers to highlight India with saffron/white/green colors, but the original code is large. I can give a short note: "Use GlobeCdn component, modify marker color to saffron and green for India (bom1)". That's not code. But they asked "DONT GIVE UR OWN CONTEXT FOR IT JUST SAY ADD ALL THIS". So the original prompt had a huge GlobeCdn code; maybe I can just mention "Add the GlobeCdn component as above (modify default markers to highlight India with saffron/white/green)". I'll quote a tiny snippet of the marker style change, but not the full component.

Goal: under 5000 characters. So I'll write a compact markdown.

I'll structure:

md
# Add all this

## Setup
```bash
...
Globe Component for Creative White
Add components/ui/globe-cdn.tsx (as given). Modify default marker for bom1 to saffron and green:

ts
// change markerColor to saffron and arcColor to green
Scroll Globe Landing Page
Add components/ui/landing-page.tsx, components/ui/demo.tsx, and the globe.tsx dependency (as given).

Tailwind CSS Animation
Add to index.css:

css
@keyframes fadeOutLabel { ... }
Background Stripes
Add components/ui/background-components.tsx with the grid/stripe code. Key snippet:

tsx
backgroundImage: `linear-gradient(...)`
Mouse Animation
Add components/ui/particle-canvas.tsx. Key snippet: WebGL particle system.

Steps to integrate
Place files in correct directories.

Install dependencies: cobe, framer-motion, etc.

Use Unsplash for globe image.

Use lucide-react for any icons.

text

But the character count might still be high. Let's calculate approximate: I'll keep it very short.

I'll include only the most necessary code lines, like the fadeOutLabel keyframes and the background gradients. For the globe-cdn, I'll say "Copy the provided GlobeCdn component; to highlight India in saffron/white/green, set baseColor to [1,1,1] and modify marker colors for India using inline style overrides." But they want "CODE + TEXT" so maybe a tiny code snippet for India: 
markerColor: [1, 0.6, 0.2], // saffron for India

text

I'll try to craft a response well under 5000 characters.

Let's draft:
Add all this
Setup
bash
git clone git@github.com:christophacham/agent-skills-library.git
gh repo clone nextlevelbuilder/ui-ux-pro-max-skill
npm install framer-motion
Creative‑White Globe (India Saffron/White/Green)
Place the GlobeCdn component in components/ui/globe-cdn.tsx. Modify the default marker for India (bom1) to saffron and green:

ts
// Inside createGlobe config:
markerColor: [1, 0.6, 0.2], // saffron
arcColor: [0.13, 0.59, 0.13], // green
If using the globe image version, set baseColor to white and adjust the overlay.

Scroll‑driven Globe Landing Page
Place these files:

components/ui/globe.tsx (CSS‑only rotating globe with stars)

components/ui/landing-page.tsx (ScrollGlobe + demo sections)

components/ui/demo.tsx (imports the demo)

Update index.css (Tailwind 4) or globals.css (Tailwind 3) with:

css
@import "tailwindcss";
@import "tw-animate-css";

@keyframes fadeOutLabel {
  0% { opacity: 1; transform: translateX(0) scale(1); }
  70% { opacity: 1; transform: translateX(0) scale(1); }
  100% { opacity: 0; transform: translateX(0.5rem) scale(0.95); }
}
Background Stripes & Glow
components/ui/background-components.tsx – provides a grid background and soft yellow glow. Combine them:

tsx
<div className="min-h-screen relative bg-white">
  <div className="absolute inset-0 z-0" style={{
    backgroundImage: `radial-gradient(circle at center, #FFF991 0%, transparent 70%),
                      linear-gradient(to right, #e5e7eb 1px, transparent 1px),
                      linear-gradient(to bottom, #e5e7eb 1px, transparent 1px)`,
    backgroundSize: "100% 100%, 40px 40px, 40px 40px"
  }} />
</div>
Mouse Particle Animation
components/ui/particle-canvas.tsx – WebGL rainbow particle trail that follows the mouse. Key part:

tsx
import { ParticleCanvas } from "@/components/ui/particle-canvas";
// Place <ParticleCanvas /> inside a relative container with pointer-events:none
Integration
Copy all files to components/ui/.

Install cobe and framer-motion.

Replace the globe image URL if needed (use a high‑res Earth texture from Unsplash).

Use lucide-react icons where required.

text

Let's count characters: about 1700. That's well under 5000. Good. I'll output this.
Add all this
Setup
bash
git clone git@github.com:christophacham/agent-skills-library.git
gh repo clone nextlevelbuilder/ui-ux-pro-max-skill
npm install framer-motion
Creative‑White Globe (India Saffron/White/Green)
Place the GlobeCdn component in components/ui/globe-cdn.tsx. Modify the default marker for India (bom1) to saffron and green:

ts
// Inside createGlobe config:
markerColor: [1, 0.6, 0.2], // saffron
arcColor: [0.13, 0.59, 0.13], // green
If using the globe image version, set baseColor to white and adjust the overlay.

Scroll‑driven Globe Landing Page
Place these files:

components/ui/globe.tsx (CSS‑only rotating globe with stars)

components/ui/landing-page.tsx (ScrollGlobe + demo sections)

components/ui/demo.tsx (imports the demo)

Update index.css (Tailwind 4) or globals.css (Tailwind 3) with:

css
@import "tailwindcss";
@import "tw-animate-css";

@keyframes fadeOutLabel {
  0% { opacity: 1; transform: translateX(0) scale(1); }
  70% { opacity: 1; transform: translateX(0) scale(1); }
  100% { opacity: 0; transform: translateX(0.5rem) scale(0.95); }
}
Background Stripes & Glow
components/ui/background-components.tsx – provides a grid background and soft yellow glow. Combine them:

tsx
<div className="min-h-screen relative bg-white">
  <div className="absolute inset-0 z-0" style={{
    backgroundImage: `radial-gradient(circle at center, #FFF991 0%, transparent 70%),
                      linear-gradient(to right, #e5e7eb 1px, transparent 1px),
                      linear-gradient(to bottom, #e5e7eb 1px, transparent 1px)`,
    backgroundSize: "100% 100%, 40px 40px, 40px 40px"
  }} />
</div>
Mouse Particle Animation
components/ui/particle-canvas.tsx – WebGL rainbow particle trail that follows the mouse. Key part:

tsx
import { ParticleCanvas } from "@/components/ui/particle-canvas";
// Place <ParticleCanvas /> inside a relative container with pointer-events:none
Integration
Copy all files to components/ui/.

Install cobe and framer-motion.

Replace the globe image URL if needed (use a high‑res Earth texture from Unsplash).

Use lucide-react icons where required.

