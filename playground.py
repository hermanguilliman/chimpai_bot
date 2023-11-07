from openai import AsyncOpenAI
import asyncio

client = AsyncOpenAI(api_key="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")

async def main():
    

    response = await client.audio.speech.create(
    model="tts-1",
    voice="shimmer",
    speed=0.8,
    input="О да",
    response_format='opus',
    )
    response.stream_to_file('shimmer.ogg')

if __name__ == "__main__":
    asyncio.run(main())