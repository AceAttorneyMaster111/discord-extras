"""discord-extras: Some helper functions for the library discord.py.

Functions: get_user_identifier: Get the unique identifier of a user, in the form User#1234.
           ask_for_message (coroutine): Ask a question to the author of a message, wait for a response, and check it against criteria.

See the specific function documentation for more details."""

import asyncio
import discord
import re

def get_user_identifier(user):
	""" get_user_identifier(user): Get the unique identifier of the discord.User or discord.Member user, in the format of User#1234."""
	try:
		return user.name + "#" + user.discriminator
	except AttributeError as a:
		raise TypeError("Expected 'discord.User' or 'discord.Member'. Received " + re.match(r"'[a-zA-Z]*'", str(a))[0])

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
		await client.send_message(message.channel, prompt)
		answer = await client.wait_for_message(channel=message.channel, author=message.author, timeout=timeout)
		if answer is None:
			await client.send_message(message.channel, timeout_msg)
			return None
		if not condition(answer.content):
			await client.send_message(message.channel, fail_msg)
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