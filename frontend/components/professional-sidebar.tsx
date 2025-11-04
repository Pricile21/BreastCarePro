"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Activity, LayoutDashboard, Upload, FileText, Users, Settings, LogOut, Menu, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { useAuth } from "@/contexts/auth-context"
import { useCurrentProfessional } from "@/hooks/use-api"

const navigation = [
  { name: "Tableau de bord", href: "/professional/dashboard", icon: LayoutDashboard },
  { name: "Nouvelle analyse", href: "/professional/upload", icon: Upload },
  { name: "Rapports", href: "/professional/reports", icon: FileText },
  { name: "Patients", href: "/professional/patients", icon: Users },
  { name: "Paramètres", href: "/professional/settings", icon: Settings },
]

export function ProfessionalSidebar() {
  const pathname = usePathname()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const { user } = useAuth()
  const { professional } = useCurrentProfessional()

  return (
    <>
      <button
        onClick={() => setIsMobileMenuOpen(true)}
        className="md:hidden fixed top-4 left-4 z-40 p-2 rounded-lg bg-card border shadow-lg"
        aria-label="Ouvrir le menu"
      >
        <Menu className="h-6 w-6" />
      </button>

      {isMobileMenuOpen && (
        <div className="md:hidden fixed inset-0 bg-black/50 z-40" onClick={() => setIsMobileMenuOpen(false)} />
      )}

      <div
        className={cn(
          "flex h-screen w-64 flex-col border-r bg-card transition-transform duration-300 ease-in-out",
          "md:translate-x-0 md:static md:z-auto",
          "fixed top-0 left-0 z-50",
          isMobileMenuOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        {/* Logo */}
        <div className="flex h-16 items-center gap-2 border-b px-6">
          <button
            onClick={() => setIsMobileMenuOpen(false)}
            className="md:hidden mr-2 p-1 hover:bg-accent rounded"
            aria-label="Fermer le menu"
          >
            <X className="h-5 w-5" />
          </button>
          <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
            <Activity className="w-5 h-5 text-primary-foreground" />
          </div>
          <span className="font-semibold">BreastCare Pro</span>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 p-4">
          {navigation.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link
                key={item.name}
                href={item.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
                )}
              >
                <item.icon className="h-5 w-5" />
                {item.name}
              </Link>
            )
          })}
        </nav>

        {/* User Section */}
        <div className="border-t p-4">
          <div className="mb-3 px-3">
            <p className="text-sm font-medium">{professional?.full_name || user?.full_name || "Utilisateur"}</p>
            <p className="text-xs text-muted-foreground">{professional?.specialty || "Professionnel de santé"}</p>
          </div>
          <Button variant="ghost" className="w-full justify-start text-muted-foreground" asChild>
            <Link href="/" onClick={() => setIsMobileMenuOpen(false)}>
              <LogOut className="mr-2 h-4 w-4" />
              Déconnexion
            </Link>
          </Button>
        </div>
      </div>
    </>
  )
}
