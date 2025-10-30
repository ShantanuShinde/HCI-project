import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { text } = await request.json()

    const response = await fetch('http://localhost:8000/moderate_unfiltered', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    })
    
    const data = await response.json()

    const isAppropriate = data.inappropriate === false

    return NextResponse.json({ isAppropriate })
  } catch (error) {
    console.error("Moderation API error:", error)
    return NextResponse.json({ error: "Moderation check failed" }, { status: 500 })
  }
}
