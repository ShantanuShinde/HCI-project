import { NextResponse } from "next/server"

export async function POST(request: Request) {
  try {
    const { text } = await request.json()

    const response = await fetch('http://localhost:8000/report_appropriate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    })

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error("Appeal API error:", error)
    return NextResponse.json({ error: "Failed to submit appeal" }, { status: 500 })
  }
}
