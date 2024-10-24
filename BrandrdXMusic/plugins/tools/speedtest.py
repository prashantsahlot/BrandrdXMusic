import asyncio
import speedtest
from pyrogram import Client, filters
from pyrogram.types import Message

from BrandrdXMusic import app
from BrandrdXMusic.misc import SUDOERS
from BrandrdXMusic.utils.decorators.language import language

# Speed test function
def testspeed(m, _):
    try:
        # Speedtest instance
        test = speedtest.Speedtest()

        # Get the best server
        test.get_best_server()

        # Notify progress
        m = m.edit_text(_["server_12"])

        # Perform download test
        test.download()

        # Notify progress
        m = m.edit_text(_["server_13"])

        # Perform upload test
        test.upload()

        # Share results
        test.results.share()

        # Get result as dictionary
        result = test.results.dict()

        # Final notification
        m = m.edit_text(_["server_14"])
    
    except Exception as e:
        return m.edit_text(f"<code>{e}</code>")

    return result

# Command handler for speed test
@app.on_message(filters.command(["speedtest", "spt"]) & SUDOERS)
@language
async def speedtest_function(client: Client, message: Message, _):
    m = await message.reply_text(_["server_11"])

    # Run speed test in separate thread
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m, _)

    if isinstance(result, dict):
        output = _["server_15"].format(
            result["client"]["isp"],
            result["client"]["country"],
            result["server"]["name"],
            result["server"]["country"],
            result["server"]["cc"],
            result["server"]["sponsor"],
            result["server"]["latency"],
            result["ping"],
        )
        
        # Send speed test result as a photo
        await message.reply_photo(photo=result["share"], caption=output)
        await m.delete()
    else:
        await m.edit_text(f"Error: Unexpected result: {result}")

