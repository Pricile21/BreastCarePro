import { redirect } from 'next/navigation'

export default function HomePage() {
  // Rediriger vers la page mobile par défaut
  redirect('/mobile')
}
