"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Progress } from "@/components/ui/progress"
import { Heart, ArrowLeft, ArrowRight } from "lucide-react"

const questions = [
  {
    id: "age",
    question: "Quel est votre âge?",
    type: "number",
    placeholder: "Ex: 35",
  },
  {
    id: "first_degree_relatives",
    question: "Votre mère ou l'une de vos sœurs a-t-elle eu un cancer du sein?",
    type: "select",
    options: [
      { label: "Non, aucune", value: 0 },
      { label: "Oui, une (mère OU une sœur)", value: 1 },
      { label: "Oui, deux ou plus (mère ET sœur, ou plusieurs sœurs)", value: 2 },
    ],
    help: "Comptez seulement votre mère et vos sœurs biologiques",
  },
  {
    id: "previous_biopsies",
    question: "Avez-vous déjà eu un examen médical où un médecin a prélevé un petit morceau de votre sein pour l'analyser?",
    type: "select",
    options: [
      { label: "Non, jamais", value: 0 },
      { label: "Oui, une fois", value: 1 },
      { label: "Oui, plusieurs fois", value: 2 },
    ],
    help: "Si vous n'êtes pas sûre ou ne vous souvenez pas, répondez 'Non' - c'est normal, beaucoup de femmes n'en ont jamais eu",
  },
  {
    id: "atypical_hyperplasia",
    question: "Si vous avez eu un prélèvement du sein, un médecin vous a-t-il dit que les cellules n'étaient pas tout à fait normales (mais que ce n'était pas un cancer)?",
    type: "boolean",
    help: "Si vous n'avez jamais eu de prélèvement ou ne savez pas, répondez 'Non' - c'est très rare",
    showIf: "previous_biopsies",
  },
  {
    id: "age_menarche",
    question: "À quel âge avez-vous eu vos premières règles?",
    type: "select",
    options: [
      { label: "Avant 12 ans", value: "<12" },
      { label: "Entre 12 et 13 ans", value: "12-13" },
      { label: "14 ans ou plus", value: "14+" },
    ],
  },
  {
    id: "age_first_birth",
    question: "À quel âge avez-vous eu votre premier enfant?",
    type: "select",
    options: [
      { label: "Avant 20 ans", value: "<20" },
      { label: "Entre 20 et 24 ans", value: "20-24" },
      { label: "Entre 25 et 29 ans", value: "25-29" },
      { label: "30 ans ou plus", value: "30+" },
      { label: "Je n'ai pas d'enfant", value: "nulliparous" },
    ],
  },
  // Section mode de vie
  {
    id: "weight_kg",
    question: "Quel est votre poids actuel?",
    type: "number",
    placeholder: "Ex: 65",
    section: "mode_de_vie",
    unit: "kg",
    help: "En kilogrammes",
  },
  {
    id: "height_cm",
    question: "Quelle est votre taille?",
    type: "number",
    placeholder: "Ex: 170",
    section: "mode_de_vie",
    unit: "cm",
    help: "En centimètres. Exemple : 1 mètre 70 = 170 cm",
    showIf: "weight_kg",
  },
  {
    id: "alcohol_consumption",
    question: "Combien de verres d'alcool buvez-vous par semaine?",
    type: "number",
    placeholder: "Ex: 0",
    section: "mode_de_vie",
    help: "1 verre = 1 verre de vin, 1 bière, ou 1 shot. Si vous ne buvez pas, écrivez 0",
  },
  {
    id: "exercise_minutes_per_week",
    question: "Combien de minutes par semaine faites-vous de sport ou d'exercice physique?",
    type: "number",
    placeholder: "Ex: 150",
    section: "mode_de_vie",
    help: "Marche rapide, vélo, natation, course, gym, etc. Si vous ne faites pas de sport, écrivez 0",
  },
  {
    id: "smoking_status",
    question: "Fumez-vous actuellement?",
    type: "select",
    options: [
      { label: "Non, je n'ai jamais fumé", value: "never" },
      { label: "Non, j'ai arrêté de fumer", value: "former" },
      { label: "Oui, je fume actuellement", value: "current" },
    ],
    section: "mode_de_vie",
    help: "Le tabac peut augmenter le risque de cancer",
  },
  {
    id: "hormone_therapy",
    question: "Prenez-vous un traitement hormonal pour la ménopause (pilules ou patchs)?",
    type: "boolean",
    section: "mode_de_vie",
    help: "Seulement si vous êtes ménopausée et prenez un traitement hormonal prescrit par un médecin",
    showIf: "age",
    showIfCondition: (age: number) => age >= 50,
  },
]

export default function AssessmentPage() {
  const router = useRouter()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string | number>>({})
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Check if user is authenticated
  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
    if (token) {
      setIsAuthenticated(true)
    } else {
      // Redirect to login if not authenticated
      router.push('/mobile/login?redirect=/mobile/assessment')
    }
  }, [router])

  // Filtrer les questions selon les conditions
  const getVisibleQuestions = () => {
    return questions.filter((q) => {
      // Questions conditionnelles basées sur showIf
      if (q.showIf) {
        const conditionAnswer = answers[q.showIf]
        
        // Afficher atypical_hyperplasia seulement si previous_biopsies > 0
        if (q.id === "atypical_hyperplasia") {
          return conditionAnswer !== undefined && conditionAnswer > 0
        }
        
        // Afficher height_cm seulement si weight_kg est fourni
        if (q.id === "height_cm") {
          return conditionAnswer !== undefined && conditionAnswer !== ""
        }
        
        // Afficher hormone_therapy seulement si age >= 50
        if (q.id === "hormone_therapy" && q.showIfCondition) {
          const age = answers.age
          return age !== undefined && q.showIfCondition(typeof age === 'number' ? age : parseInt(age as string))
        }
      }
      
      return true
    })
  }

  const visibleQuestions = getVisibleQuestions()
  // Trouver la question actuelle dans la liste visible
  const currentQuestionInVisible = Math.max(0, visibleQuestions.findIndex(q => q.id === questions[currentQuestion]?.id))
  const currentQ = visibleQuestions[currentQuestionInVisible >= 0 ? currentQuestionInVisible : 0] || questions[0]
  const progress = visibleQuestions.length > 0 ? ((currentQuestionInVisible + 1) / visibleQuestions.length) * 100 : 0

  const handleAnswer = (answer: string | number) => {
    setAnswers({ ...answers, [currentQ.id]: answer })
  }

  const isAnswerValid = () => {
    // Vérifier si la question doit être affichée (questions conditionnelles)
    if (currentQ.showIf && answers[currentQ.showIf] === undefined) {
      return true // On peut passer si la condition n'est pas remplie
    }
    // Toutes les questions affichées doivent être obligatoires
    // Vérifier que la réponse existe
    const answer = answers[currentQ.id]
    // Accepter 0, false, ou toute chaîne non vide comme valeur valide
    return answer !== undefined && answer !== ""
  }

  const getRiskData = () => {
    const riskData: any = {
      age: parseInt(String(answers.age)) || 50,
      first_degree_relatives: parseInt(String(answers.first_degree_relatives)) || 0,
      previous_biopsies: parseInt(String(answers.previous_biopsies)) || 0,
      atypical_hyperplasia: answers.atypical_hyperplasia === true || answers.atypical_hyperplasia === "true",
      age_menarche: answers.age_menarche as string || "12-13",
      age_first_birth: answers.age_first_birth as string || "25-29",
    }
    
    // Ajouter les facteurs de mode de vie s'ils sont fournis
    if (answers.weight_kg) riskData.weight_kg = parseFloat(String(answers.weight_kg))
    if (answers.height_cm) riskData.height_cm = parseFloat(String(answers.height_cm))
    if (answers.alcohol_consumption !== undefined) riskData.alcohol_consumption = parseInt(String(answers.alcohol_consumption)) || 0
    if (answers.exercise_minutes_per_week !== undefined) riskData.exercise_minutes_per_week = parseInt(String(answers.exercise_minutes_per_week)) || 0
    if (answers.smoking_status) riskData.smoking_status = answers.smoking_status as string
    if (answers.hormone_therapy !== undefined) riskData.hormone_therapy = answers.hormone_therapy === true || answers.hormone_therapy === "true"
    
    return riskData
  }

  const handleNext = () => {
    if (!isAnswerValid()) return
    
    // Navigation normale - passer à la prochaine question visible
    if (currentQuestionInVisible < visibleQuestions.length - 1) {
      const nextVisibleIndex = currentQuestionInVisible + 1
      const nextQuestion = visibleQuestions[nextVisibleIndex]
      if (nextQuestion) {
        const actualIndex = questions.findIndex(q => q.id === nextQuestion.id)
        if (actualIndex !== -1) {
          setCurrentQuestion(actualIndex)
        }
      }
    } else {
      // Fin du questionnaire - préparer et envoyer les données
      const riskData = getRiskData()
      sessionStorage.setItem('riskAssessmentData', JSON.stringify(riskData))
      router.push(`/mobile/assessment/results`)
    }
  }

  const handleBack = () => {
    if (currentQuestionInVisible > 0) {
      // Revenir à la question précédente visible
      const prevVisibleIndex = currentQuestionInVisible - 1
      const prevQuestion = visibleQuestions[prevVisibleIndex]
      if (prevQuestion) {
        const actualIndex = questions.findIndex(q => q.id === prevQuestion.id)
        if (actualIndex !== -1) {
          setCurrentQuestion(actualIndex)
        }
      }
    }
  }

  // Don't render content if not authenticated
  if (!isAuthenticated) {
    return null
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-accent/5">
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/mobile">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour
            </Link>
          </Button>
          <div className="flex items-center gap-2">
            <Heart className="w-5 h-5 text-accent" />
            <span className="font-semibold">Évaluation</span>
          </div>
          <div className="w-20" />
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-2xl">
        {/* Progress */}
        <div className="mb-8">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-muted-foreground">
              Question {currentQuestionInVisible + 1} sur {visibleQuestions.length}
            </span>
            <span className="font-medium">{Math.round(progress)}%</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Question Card */}
        <Card className="border-2">
          <CardHeader>
            <CardTitle className="text-2xl text-balance">{currentQ.question}</CardTitle>
            <CardDescription>
              {currentQ.type === "number" 
                ? "Entrez votre réponse" 
                : currentQ.type === "boolean"
                ? "Sélectionnez Oui ou Non"
                : "Sélectionnez la réponse qui vous correspond"}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {currentQ.type === "number" ? (
              <div className="space-y-4">
                {currentQ.unit && (
                  <div className="flex items-center gap-2">
                    <Input
                      type="number"
                      placeholder={currentQ.placeholder || "Entrez un nombre"}
                      value={answers[currentQ.id] !== undefined ? answers[currentQ.id] : ""}
                      onChange={(e) => {
                        const inputValue = e.target.value
                        if (inputValue === "" || inputValue === null) {
                          const newAnswers = { ...answers }
                          delete newAnswers[currentQ.id]
                          setAnswers(newAnswers)
                        } else {
                          const val = currentQ.unit === "kg" || currentQ.unit === "cm" 
                            ? parseFloat(inputValue)
                            : parseInt(inputValue)
                          if (!isNaN(val)) {
                            handleAnswer(val)
                          }
                        }
                      }}
                      className="text-lg flex-1"
                      min={currentQ.id === "weight_kg" ? 30 : currentQ.id === "height_cm" ? 100 : currentQ.id === "age" ? 18 : 0}
                      max={currentQ.id === "weight_kg" ? 200 : currentQ.id === "height_cm" ? 250 : currentQ.id === "age" ? 90 : 1000}
                    />
                    <span className="text-sm text-muted-foreground font-medium">{currentQ.unit}</span>
                  </div>
                )}
                {!currentQ.unit && (
                  <Input
                    type="number"
                    placeholder={currentQ.placeholder || "Entrez un nombre"}
                    value={answers[currentQ.id] !== undefined ? answers[currentQ.id] : ""}
                    onChange={(e) => {
                      const inputValue = e.target.value
                      if (inputValue === "" || inputValue === null) {
                        // Champ vide - supprimer la réponse
                        const newAnswers = { ...answers }
                        delete newAnswers[currentQ.id]
                        setAnswers(newAnswers)
                      } else {
                        const val = parseInt(inputValue)
                        if (!isNaN(val)) {
                          handleAnswer(val)
                        }
                      }
                    }}
                    className="text-lg"
                    min={currentQ.id === "age" ? 18 : 0}
                    max={currentQ.id === "age" ? 90 : currentQ.id === "exercise_minutes_per_week" ? 1000 : 50}
                  />
                )}
              </div>
            ) : currentQ.type === "boolean" ? (
              <RadioGroup 
                value={answers[currentQ.id] !== undefined ? String(answers[currentQ.id]) : ""} 
                onValueChange={(value) => handleAnswer(value === "true")}
              >
                <div className="space-y-3">
                  <div className="flex items-center space-x-3 p-4 rounded-lg border hover:bg-accent/5">
                    <RadioGroupItem value="false" id="boolean-false" />
                    <Label htmlFor="boolean-false" className="flex-1 cursor-pointer">Non</Label>
                  </div>
                  <div className="flex items-center space-x-3 p-4 rounded-lg border hover:bg-accent/5">
                    <RadioGroupItem value="true" id="boolean-true" />
                    <Label htmlFor="boolean-true" className="flex-1 cursor-pointer">Oui</Label>
                  </div>
                </div>
              </RadioGroup>
            ) : (
              <RadioGroup 
                value={answers[currentQ.id] !== undefined ? String(answers[currentQ.id]) : ""} 
                onValueChange={(value) => {
                  // Convertir en nombre si c'est un select avec des valeurs numériques
                  const numValue = parseInt(value)
                  handleAnswer(!isNaN(numValue) && value === String(numValue) ? numValue : value)
                }}
              >
              <div className="space-y-3">
                  {currentQ.options?.map((option: any, index: number) => (
                  <div key={index} className="flex items-center space-x-3 p-4 rounded-lg border hover:bg-accent/5">
                      <RadioGroupItem value={String(option.value)} id={`option-${index}`} />
                    <Label htmlFor={`option-${index}`} className="flex-1 cursor-pointer">
                        {option.label}
                    </Label>
                  </div>
                ))}
              </div>
            </RadioGroup>
            )}
            {currentQ.help && (
              <p className="text-sm text-muted-foreground mt-4">{currentQ.help}</p>
            )}
          </CardContent>
        </Card>

        {/* Navigation */}
        <div className="flex gap-4 mt-8">
          <Button
            variant="outline"
            onClick={handleBack}
            disabled={currentQuestionInVisible === 0}
            className="flex-1 bg-transparent"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Précédent
          </Button>
          <Button
            onClick={handleNext}
            disabled={!isAnswerValid()}
            className="flex-1 bg-accent hover:bg-accent/90 text-accent-foreground"
          >
            {currentQuestionInVisible >= visibleQuestions.length - 1 ? "Voir les résultats" : "Suivant"}
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </main>
    </div>
  )
}
