from pyini_parser.configure.parser import ConfigParser

from components import BASE_DIR


class TestPlanTemp:
    """
    This class only to set something like plan temps to user
    """

    @staticmethod
    def create_temps():
        config = ConfigParser()
        result = []
        with open(f"{BASE_DIR}/server/temps.ini", "r") as file:
            temps = config.read(file)
            for section in list(temps):
                result.append(
                    {
                        "title": section.replace("_", " "),
                        "content": temps.pop(section)["content"],
                    }
                )
        return result
