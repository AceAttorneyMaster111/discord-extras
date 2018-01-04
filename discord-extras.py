"""discord-extras: Some helper functions for the library discord.py.

Functions: get_user_identifier: Get the unique identifier of a user, in the form User#1234.
           ask_for_message (coroutine): Ask a question to the author of a message, wait for a response, and check it against criteria.
           reply (coroutine): Send a reply to the channel of a message.

Classes: Client: A subclass of discord.Client that incorporates additional methods.

See the specific function documentation for more details."""

import asyncio
import discord
import re

def get_user_identifier(user):
	"""get_user_identifier(user): Get the unique identifier of the discord.User or discord.Member user, in the format of User#1234."""
	try:
		return user.name + "#" + user.discriminator
	except AttributeError as a:
		raise TypeError("Expected 'discord.User' or 'discord.Member'. Received " + re.match(r"'[a-zA-Z]*'", str(a))[0])

async def reply(client, message, text):
	"""reply(client, message, text): Shrinks needed code for sending a reply to a message's channel.

This function is a coroutine. (must be used with await).

Params: client (discord.Client): The client from which to send message.
        message (discord.Message): The message being replied to.
        text (str): The text for the reply."""
    await client.send_message(message.channel, text)

async def ask_for_message(client, message, prompt, timeout=30, timeout_msg="Operation timed out.", condition=lambda m: True, fail_msg=""):
	"""ask_for_message(client, message, prompt, timeout=30, timeout_msg="Operation timed out.". condition=lambda m: True, fail_msg=""):

Shrinks needed code for getting input from user.

This function is a coroutine. (must be used with await)

Params: client (discord.Client): The client from which to ask
        message (discord.Message): The original message being responded to
        prompt (str): The question to ask the user
Keyword params:
        timeout (int): The amount of time in seconds to give the user to answer.
        	Defaults to 30.
        timeout_msg (str): The message to display to the user if they don't answer in the required amount of time.
        	Defaults to "Operation timed out."
        condition (lambda(str): bool): The condition to pass the user's answer through.
        	Defaults to letting all answers pass. (lambda m: True)
        fail_msg (str): The message to display to the user if their response returns False when passed through condition.
        	Defaults to an empty string. ("")

Returns: str containing message content, otherwise None if condition failed or timeout_msg was sent.

More detail: The client sends a message to message.channel containing prompt, then waits for a response from message.author for timeout seconds.
	         If the author sends nothing in response, the client sends another message containing timeout_msg.
	         Otherwiser, the message's content will be passed through condition. If it returns False, the client will send fail_msg."""
	try:
		assert isinstance(timeout, int)
		await reply(client, message.channel, prompt)
		answer = await client.wait_for_message(channel=message.channel, author=message.author, timeout=timeout)
		if answer is None:
			await reply(client, message.channel, timeout_msg)
			return None
		if not condition(answer.content):
			await reply(client, message.channel, fail_msg)
			return None
		return message.content
	except Exception as e:
		if isinstance(e, AttributeError):
			try:
				assert isinstance(client, discord.Client)
			except AssertionError:
				errtype = "discord.Client"
			else:
				errtype = "discord.Message"
			# client, message
		elif isinstance(e, TypeError):
			errtype = "lambda"
			# condition
		elif isinstance(e, AssertionError):
			errtype = "int"
			# timeout
		raise TypeError(("Expected '{}'. Received " + re.match(r"'[a-zA-Z]*'", str(a))[0]).format(errtype))

class Client(discord.Client):
	"""Client: A subclass of discord.Client that incorporates additional methods.

Params: none

Methods: ask_for_message: Ask a question to the author of a message, wait for a response, and check it against criteria.
	     reply: A shortcut for client.send_message"""
	async def ask_for_message(self, message, prompt, timeout=30, timeout_msg="Operation timed out.", condition=lambda m: True, fail_msg=""):
		"""ask_for_message(message, prompt, timeout=30, timeout_msg="Operation timed out.". condition=lambda m: True, fail_msg=""):

An alias for the module-level ask_for_message. Shrinks needed code for getting input from user.

This method is a coroutine. (must be used with await)

Params: message (discord.Message): The original message being responded to
        prompt (str): The question to ask the user
Keyword params:
        timeout (int): The amount of time in seconds to give the user to answer.
        	Defaults to 30.
        timeout_msg (str): The message to display to the user if they don't answer in the required amount of time.
        	Defaults to "Operation timed out."
        condition (lambda(str): bool): The condition to pass the user's answer through.
        	Defaults to letting all answers pass. (lambda m: True)
        fail_msg (str): The message to display to the user if their response returns False when passed through condition.
        	Defaults to an empty string. ("")

Returns: str containing message content, otherwise None if condition failed or timeout_msg was sent.

More detail: The client sends a message to message.channel containing prompt, then waits for a response from message.author for timeout seconds.
	         If the author sends nothing in response, the client sends another message containing timeout_msg.
	         Otherwiser, the message's content will be passed through condition. If it returns False, the client will send fail_msg."""
	    try:
			assert isinstance(timeout, int)
			await reply(self, message.channel, prompt)
			answer = await self.wait_for_message(channel=message.channel, author=message.author, timeout=timeout)
			if answer is None:
				await reply(self, message.channel, timeout_msg)
				return None
			if not condition(answer.content):
				await reply(self, message.channel, fail_msg)
				return None
			return message.content
		except Exception as e:
			if isinstance(e, AttributeError):
				errtype = "discord.Message"
				# message
			elif isinstance(e, TypeError):
				errtype = "lambda"
				# condition
			elif isinstance(e, AssertionError):
				errtype = "int"
				# timeout
			raise TypeError(("Expected '{}'. Received " + re.match(r"'[a-zA-Z]*'", str(a))[0]).format(errtype))
	async def reply(self, message, text):
		"""reply(message, text): An alias for the module-level reply. Shrinks needed code for sending a reply to a message's channel.

This method is a coroutine. (must be used with await).

Params: client (discord.Client): The client from which to send message.
        message (discord.Message): The message being replied to.
        text (str): The text for the reply."""
        await self.send_message(message.channel, text)