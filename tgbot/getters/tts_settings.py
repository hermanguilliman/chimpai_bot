from aiogram_dialog import DialogManager


async def tts_models_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "tts_models": [
            "tts-1",
            "tts-1-hd",
        ]
    }


async def voices_names_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "tts_voices": [
            "alloy",
            "echo",
            "fable",
            "onyx",
            "nova",
            "shimmer",
        ]
    }


async def get_tts_speed(dialog_manager: DialogManager, **kwargs):
    if len(dialog_manager.dialog_data) == 0:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
    return dialog_manager.dialog_data
