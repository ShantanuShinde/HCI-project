import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { text } = await request.json()

    const response = await fetch('http://localhost:8000/report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    })


    return response;
  } catch (error) {
    console.error("Report API error:", error)
    return NextResponse.json({ error: "Report submission failed" }, { status: 500 })
  }
}
