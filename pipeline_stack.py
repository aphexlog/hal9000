#!/usr/bin/env python3
from constructs import Construct

from aws_cdk import Stack, Stage, CfnOutput

from aws_cdk.pipelines import (
    CodePipeline,
    CodePipelineSource,
    ShellStep,
)

from application_stack import ChatbotStack, ChatbotStackProps


class ApplicationStageChatbot(Stage):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        chatbot_props: ChatbotStackProps,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ChatbotStack(self, "hal9000-chatbot", props=chatbot_props)


class PipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create ChatbotStackProps
        chatbot_props = ChatbotStackProps(
            slack_workspace_id="your_slack_workspace_id",
            slack_channel_id="your_slack_channel_id",
        )

        pipeline = CodePipeline(
            self,
            "Pipeline",
            synth=ShellStep(
                "Synth",
                input=CodePipelineSource.connection(
                    "elevator-robot/hal9000",
                    "main",
                    connection_arn="arn:aws:codestar-connections:us-east-1:764114738171:connection/ea715684-208a-4756-ac77-b1ab5acd5dfe",  # noqa: E501
                ),
                commands=["pip install -r requirements.txt", "cdk synth"],
            ),
            self_mutation=False,
        )

        pipeline.add_stage(
            ApplicationStageChatbot(
                self,
                "ChatbotStage",
                chatbot_props=chatbot_props,
            )
        )

        CfnOutput(self, "PipelineStack", value="PipelineStack")
