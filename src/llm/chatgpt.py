import asyncio
import random
import json
from pyppeteer import launch, connect
from pyppeteer.errors import PageError
import os
import logging
import time
import hashlib

logging.basicConfig(level=logging.INFO)


class ChatGPT:
    def __init__(self, chatbot_url='https://chat.openai.com/', headless=False, save_conversation_callback=None):
        self.browser = None
        self.page = None
        self.headless = headless
        self.chatbot_url = chatbot_url
        self.is_first_message = True
        self.last_message = ''
        self.last_reply = ''
        self.let_timeout = 1900
        self.let_timeout_xl = 190000
        self.save_conversation_callback = save_conversation_callback
        self.conversation_history = []
        self.handle_err_act = False
        # Generate a random hash and assign it to self.id
        self.id = hashlib.sha256(os.urandom(16)).hexdigest() + ".json"

    async def initialize_browser(self):
        if self.headless:
            self.browser = await launch()
        else:
            self.browser = await connect({"browserURL": "http://127.0.0.1:9222", "headless": True, "defaultViewport": {"width": 2000, "height": 800}})
        self.page = await self.browser.newPage()
        await self.page.goto(self.chatbot_url)
        logging.info('Browser initialized')

    async def random_delay(self):
        delay = random.randint(5000, 10000)
        await asyncio.sleep(delay / 1000)

    async def save_conversation_to_file(self):
        try:
            with open(self.id, 'w') as file:
                json.dump(self.conversation_history, file, indent=2)
            logging.info(f'Conversation saved to {self.id}')
        except Exception as e:
            logging.error(f'Failed to save conversation to file: {str(e)}')

    async def check_con_his(self):
        return os.path.exists(self.id)

    async def send_message(self, message, timeout=None):
        message = message.replace('\n', ' ')
        # await self.page.bringToFront()

        try:
            if self.is_first_message:
                await self.initialize_browser()
                self.is_first_message = False

            await self.page.evaluate('window.scrollBy(0, window.innerHeight);')
            await self.page.waitForSelector('#prompt-textarea', timeout=timeout or self.let_timeout)

            # await self.page. type('#prompt-textarea', message, {'delay': 60})
            dt = '''
                                     () => {
                                        document.querySelector("#prompt-textarea").value = "'''+message+'''";
                                     }
                                     '''
            
            await self.page.evaluate(dt)
            await self.page. type('#prompt-textarea', " ", {'delay': 60})
            await self.page.waitForSelector('[data-testid="fruitjuice-send-button"]', timeout=self.let_timeout_xl)
            await self.page.click('[data-testid="fruitjuice-send-button"]')

            self.last_message = message
            self.conversation_history.append(f'message : {message} \n')

        except PageError as e:
            logging.error(f'Error: {str(e)}')
            await self.handle_error()

    async def get_reply(self, timeout=None):
        # await self.page.bringToFront()
        await self.page.evaluate('window.scrollBy(0, window.innerHeight);')
        await self.random_delay()

        try:
            await self.page.waitForSelector('[data-testid="fruitjuice-send-button"]', timeout=timeout or self.let_timeout_xl)
            await self.page.waitForSelector('div[data-message-author-role="assistant"]', timeout=timeout or self.let_timeout_xl)

            reply_text = await self.page.evaluate(
                '''() => {
                    const replyElements = document.querySelectorAll('div[data-message-author-role="assistant"]');
                    const lastReplyElement = replyElements[replyElements.length - 1];
                    return lastReplyElement ? lastReplyElement.innerText : 'No reply found';
                }'''
            )

            self.last_reply = reply_text
            self.conversation_history.append(f'reply : {reply_text} \n')

            return reply_text

        except PageError as e:
            logging.error(f'Error: {str(e)}')
            return await self.handle_error()

    async def close_browser(self):
        await self.browser.close()
        logging.info('Browser closed')

    async def aquery(self, message):
        await self.send_message(message)
        # await asyncio.sleep(5)
        return await self.get_reply()

    def query(self, message):
        return self.exec_async(self.aquery, message)

    def exec_async(self, fct, *args, **kwargs):
        loop = asyncio.new_event_loop()
        future = asyncio.ensure_future(fct(*args, **kwargs))
        response = loop.run_until_complete(future)
        # loop.close()
        return response


async def main():
    chat_gpt = ChatGPT(
        chatbot_url="https://chatgpt.com/c/e37e12b2-3e45-4a0b-8197-e5b0d8ec0fe8")

    # answer= await chat_gpt.query('Hello!')
    # print(answer)

    # answer= await chat_gpt.query('Who is Obama ?')
    # print(answer)

    # await chat_gpt.close_browser()

if __name__ == '__main__':
    asyncio.run(main())
