import httpx
import asyncio

async def main():
    print(f"httpx version: {httpx.__version__}")
    try:
        async with httpx.AsyncClient(proxy="http://127.0.0.1:7890") as client:
            print("proxy arg works")
    except Exception as e:
        print(f"proxy arg failed: {e}")
        
    try:
        async with httpx.AsyncClient(proxies="http://127.0.0.1:7890") as client:
            print("proxies arg works")
    except Exception as e:
        print(f"proxies arg failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
