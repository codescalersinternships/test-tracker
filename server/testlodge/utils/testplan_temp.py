from pyini_parser.configure.parser import ConfigParser
from typing import Dict
from server.testlodge.models.project import TestPlan, TestPlanDetail


class TestPlanTemp():
    """
    This class only to set something like plan temps to user
    """
    def __init__(self, plan: TestPlan):
        """This function to set the plan"""
        self.plan = plan
    
    def create_temps(self):
        config = ConfigParser()
        temps = config.read('temps.ini')
        for temp, items in temps.items():
            for detail, value in items.items():
                TestPlanDetail.objects.create(
                    name = temp,
                    content = items[value]
                )
        return