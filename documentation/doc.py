"""
Simulate the workflow of the example
"""
import Components

workflow = Components.Workflow("workflow_1")
print("Creating workflow")
print(workflow)

step_1 = Components.Step("Status 1")
workflow.add_step(step_1)

print("Adding Status 1")
print(workflow)

step_2 = Components.Step("Status 2")
workflow.add_step(step_2)

print("Adding Status 2")
print(workflow)

step_3 = Components.Step("Validated")
workflow.add_step(step_3)

print("Adding Status 3")
print(workflow)

print("\n Creating Project 1")
project_1 = Components.item_factory(item_type="PROJECT", item_name="Project 1", item_step=None, video="video1")
print(project_1)

print("Adding Project 1 to Workflow 1")
workflow.add_item(project_1)
print(workflow)

print("Upgrading Project 1 one time")
workflow.upgrade_item(project_1)
print(workflow)

print("Upgrading Project 1 one time")
workflow.upgrade_item(project_1)
print(workflow)

print("Upgrading Project 1 one time")
workflow.upgrade_item(project_1)
print(workflow)

print("\n Creating Charter 1")
chart_1 = Components.item_factory(item_type="CHARTER", item_name="Charter 1", item_step=None, rules="Thou shoul not kill")
print(chart_1)

print("Adding Charter 1 to Workflow 1")
workflow.add_item(chart_1)
print(workflow)

print("Upgrading Charter 1 one time")
workflow.upgrade_item(chart_1)
print(workflow)

print("Downgrading Charter 1 one time")
workflow.downgrade_item(chart_1)
print(workflow)

print("Upgrading Charter 1 one time")
workflow.upgrade_item(chart_1)
print(workflow)


print("Moving Charter 1 to step 3")
workflow.move_item_to_step_index(chart_1, 3)
print(workflow)

print("Moving Charter 1 to step 5")
try:
    workflow.move_item_to_step_index(chart_1, 5)
except ValueError as e:
    print(e)
print(workflow)

print("Moving Charter 1 to step 0")
try:
    workflow.move_item_to_step_index(chart_1, 0)
except ValueError as e:
    print(e)
print(workflow)

print("\n Changing Step 1 Name")
workflow.change_step_name(1, "En cours de validation.")
print(workflow)

print("\n Changing Step 2 Name")
workflow.change_step_name(2, "Pending Pull Request.")
print(workflow)

print("\n Changing Step 3 Name")
workflow.change_step_name(3, "Done.")
print(workflow)

print("\n Changing Step 5 Name")
try:
    workflow.change_step_name(5, "Done.")
except ValueError as e:
    print(e)

print(workflow)