# Context

At runtime, the workflow execution maintain a context dictionary that manages assigned variables. In the workflow definition, there are several location where variables can be assigned into the context. These locations are input, vars, and output in the workflow model and publish in the task transition model. The order of the variables being assigned into the context dictionary at runtime goes from workflow input and workflow vars at the start of workflow execution, to publish on each task completion, then finally output on workflow completion.

Once a variable is assigned into the context dictionary, it can be referenced by a custom function named ctx. The `ctx` function takes the variable name as argument like `ctx(foobar)` or returns the entire dictionary if no argument is provided. This can be referenced by dot notation - e.g. `ctx().foobar`.

# Want to know more?
'https://docs.stackstorm.com/orquesta/context.html'


# Datastore
The goal of the datastore service is to allow users to store common parameters and their values within StackStorm for reuse in the definition of sensors, actions, and rules. The datastore service stores the data as a key-value pair. They can be get/set using the StackStorm CLI or the StackStorm Python client.

From the sensor and action plugins, since they are implemented in Python, the key-value pairs are accessed from the StackStorm Python client. For rule definitions in YAML/JSON, the key-value pairs are referenced with a specific string substitution syntax and the references are resolved on rule evaluation.

Key-Value pairs can also have a TTL associated with them, for automatic expiry.


# Update an existing key-value pair:

`st2 key set os_keystone_endpoint http://localhost:5000/v3`

# Delete an existing key-value pair:

`st2 key delete os_keystone_endpoint`

# Referencing Key-Value Pairs in Action Definitions

Key-value pairs are referenced via specific string substitution syntax in rules. In general, the variable for substitution is enclosed with double brackets (i.e. {{var1}}). To refer to a key-value pair, prefix the name with “st2kv.system”, e.g. `{{st2kv.system.os_keystone_endpoint}}`.
