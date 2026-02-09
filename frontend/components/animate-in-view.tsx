"use client"

import { useEffect, useRef, ReactNode } from "react"

interface AnimateInViewProps {
  children: ReactNode
  className?: string
  delay?: number
  rootMargin?: string
}

export function AnimateInView({ children, className = "", delay = 0, rootMargin = "0px 0px -60px 0px" }: AnimateInViewProps) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add("visible")
        })
      },
      { threshold: 0.1, rootMargin }
    )

    observer.observe(el)
    return () => observer.disconnect()
  }, [rootMargin])

  return (
    <div ref={ref} className={`animate-on-scroll ${className}`} style={{ transitionDelay: delay ? `${delay}ms` : undefined }}>
      {children}
    </div>
  )
}
