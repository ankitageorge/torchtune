# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import pytest
from tests.common import ASSETS
from torchtune.data import Message
from torchtune.models.llama2 import llama2_tokenizer


class TestLlama2Tokenizer:
    def tokenizer(self, template: bool = False):
        # m.model is a pretrained Sentencepiece model using the following command:
        # spm.SentencePieceTrainer.train('--input=<TRAIN_FILE> --model_prefix=m --vocab_size=2000')
        return llama2_tokenizer(
            str(ASSETS / "m.model"),
            prompt_template="torchtune.models.llama2.Llama2ChatTemplate"
            if template
            else None,
        )

    @pytest.fixture
    def expected_tokens(self):
        # fmt: off
        return [1, 323, 418, 202, 31, 128, 15, 120, 47, 88, 584, 23, 1665, 182, 9, 434, 295, 85, 4, 780, 47, 636, 9,
                1094, 213, 23, 9, 69, 69, 164, 1153, 299, 35, 961, 132, 237, 7, 5, 761, 4, 12, 0, 313, 120, 47, 88, 584,
                166, 493, 171, 54, 299, 9, 906, 244, 19, 186, 767, 303, 671, 92, 209, 24, 190, 52, 38, 4, 12, 0, 1243,
                7, 69, 135, 213, 166, 6, 21, 45, 128, 71, 58, 38, 14, 10, 652, 35, 462, 101, 1306, 7, 341, 171, 20, 14,
                127, 26, 652, 7, 10, 1268, 4, 6, 21, 45, 591, 9, 566, 22, 994, 913, 38, 20, 52, 24, 10, 1306, 734, 14,
                71, 365, 1382, 7, 10, 801, 105, 88, 244, 985, 7, 4, 6, 21, 45, 9, 566, 126, 180, 11, 5, 1137, 7, 10,
                1089, 151, 8, 1156, 213, 342, 7, 10, 384, 104, 54, 470, 4, 6, 21, 45, 287, 14, 33, 125, 135, 24, 101,
                512, 66, 7, 28, 822, 15, 542, 69, 59, 110, 14, 365, 229, 7, 3, 36, 267, 36, 125, 135, 24, 101, 1503,
                182, 9, 222, 1661, 191, 332, 92, 92, 24, 24, 4, 2]  # noqa
        # fmt: on

    @pytest.fixture
    def messages(self):
        return [
            Message(
                role="user",
                content="Below is an instruction that describes a task. Write a response "
                "that appropriately completes the request.\n\n### Instruction:\nGenerate "
                "a realistic dating profile bio.\n\n### Response:\n",
                masked=True,
            ),
            Message(
                role="assistant",
                content="I'm an outgoing and friendly person who loves spending time with "
                "friends and family. I'm also a big-time foodie and love trying out new "
                "restaurants and different cuisines. I'm a big fan of the arts and enjoy "
                "going to museums and galleries. I'm looking for someone who shares my "
                "interest in exploring new places, as well as someone who appreciates a "
                "good conversation over coffee.",
            ),
        ]

    def test_tokenize_messages(self, messages, expected_tokens):
        tokenizer = self.tokenizer(template=False)
        tokens, mask = tokenizer.tokenize_messages(messages)
        # Mask user, unmask assistant, add EOS token
        expected_mask = [True] * 75 + [False] * 125

        assert len(tokens) == len(mask)
        assert expected_tokens == tokens
        assert expected_mask == mask

    @pytest.mark.parametrize(
        "add_start_tokens, add_end_tokens",
        [
            (True, True),
            (False, False),
        ],
    )
    def test_tokenize_messages_chat_template(
        self, messages, add_start_tokens, add_end_tokens
    ):
        tokenizer = self.tokenizer(template=True)
        tokens, mask = tokenizer.tokenize_messages(
            messages, add_start_tokens=add_start_tokens, add_end_tokens=add_end_tokens
        )

        # fmt: off
        expected_tokens = [351, 82, 391, 221, 220, 193, 323, 418, 202, 31, 128, 15, 120, 47, 88, 584, 23, 1665, 182, 9,
                           434, 295, 85, 4, 780, 47, 636, 9, 1094, 213, 23, 9, 69, 69, 164, 1153, 299, 35, 961, 132,
                           237, 7, 5, 761, 4, 12, 0, 313, 120, 47, 88, 584, 166, 493, 171, 54, 299, 9, 906, 244, 19,
                           186, 767, 303, 671, 92, 209, 24, 190, 52, 38, 4, 12, 0, 1243, 7, 69, 135, 213, 166, 351, 0,
                           82, 391, 221, 220, 193, 6, 21, 45, 128, 71, 58, 38, 14, 10, 652, 35, 462, 101, 1306, 7, 341,
                           171, 20, 14, 127, 26, 652, 7, 10, 1268, 4, 6, 21, 45, 591, 9, 566, 22, 994, 913, 38, 20, 52,
                           24, 10, 1306, 734, 14, 71, 365, 1382, 7, 10, 801, 105, 88, 244, 985, 7, 4, 6, 21, 45, 9, 566,
                           126, 180, 11, 5, 1137, 7, 10, 1089, 151, 8, 1156, 213, 342, 7, 10, 384, 104, 54, 470, 4, 6,
                           21, 45, 287, 14, 33, 125, 135, 24, 101, 512, 66, 7, 28, 822, 15, 542, 69, 59, 110, 14, 365,
                           229, 7, 3, 36, 267, 36, 125, 135, 24, 101, 1503, 182, 9, 222, 1661, 191, 332, 92, 92, 24, 24,
                           4] # noqa
        # fmt: on

        # Mask user, unmask assistant
        expected_mask = [True] * 87 + [False] * 124

        if add_end_tokens:
            expected_tokens = expected_tokens + [tokenizer.eos_id]
            expected_mask = expected_mask + [False]

        if add_start_tokens:
            expected_tokens = [tokenizer.bos_id] + expected_tokens
            expected_mask = [True] + expected_mask

        assert expected_tokens == tokens
        assert expected_mask == mask
