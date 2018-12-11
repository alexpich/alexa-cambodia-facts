# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

SKILL_NAME = "Cambodia Facts"
GET_FACT_MESSAGE = "Here is a fact about Cambodia: "
HELP_MESSAGE = "You can say give me a fact, or, you can say stop. How can I help you?"
HELP_REPROMPT = "How can I help?"
STOP_MESSAGE = "Sok suh bye!"
FALLBACK_MESSAGE = "TODO"
FALLBACK_REPROMPT = "How can I help you?"
EXCEPTION_MESSAGE = "Sorry. I can't help with that."

data = [
  'Cambodia is a country located in the southern portion of southeast Asia and is bordered by Thailand to the northwest, Laos to the north, and Vietnam to the east.',
  'The capital of Cambodia is Phnom Penh.',
  'The country of Cambodia has a population of over fifteen million people.',
  'The official religion in Cambodia is Theravada Buddhism',
  'Cambodia gained independence in 1953',
  'Since 1955, Cambodia has been a member of the United Nations.',
  "Similar to the rest of Southeast Asia, Cambodia's climate is extremely hot and humid, with temperatures ranging from 70 to 95 degrees fahrenheit.",
  'Cambodia is known to have two distinct seasons, rainy season from May to October, and dry season from November to April.',
  'The spoken language in Cambodia is Khmer.',
  'The dominant source of income is agriculture with strong growths in textiles, construction, garments and tourism.',
  'The Khmer Rouge, a communist group, occupied Cambodia from 1975 to 1978.',
  'Angelina Jolie\'s oldest son, Maddox Jolie-Pitt, is of Cambodian heritage.',
  'Angkor Wat, located in Siem Reap, is a temple and one of the largest religious monuments in the world.',
  'Millions of land mines were planted during the war years and are still in the ground today.',
  'The Khmer Rouge enacted a genocide in Cambodia from 1975 to 1979, killing more than one and a half million people.',
  'Kampuchea is another name for Cambodia',
  'The Cambodian flag features two blue horizontal stripes surrounding a red stripe with Angkor Wat in the center.',
  'Over 5 million people visit Cambodia each year.',
  'The largest minority groups in Cambodia are Vietnamese, Chinese, and Chams.',
  'The Cambodian motto is Nation, Religion, King',
  'The language of Cambodia is Khmer.',
  'Popular sports in Cambodia are football and martial arts.',
  'The top ranking university in Cambodia is the Royal University of Phnom Penh.',
  'Rice is a staple in Cambodian cuisine.',
  'Fish is a large part of the Cambodian diet. '
  'Cambodia became a protectorate of France in 1863 and was incorporated into French Indochina in 1887.'
  
]

# =========================================================================================================================================
# Editing anything below this line might break your skill.
# =========================================================================================================================================

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class GetFactHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetNewSpaceFactIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        random_fact = random.choice(data)
        speech = GET_FACT_MESSAGE + random_fact

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, random_fact))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(GetFactHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
