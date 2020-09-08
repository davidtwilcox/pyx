<!-- PROJECT LOGO -->
<p align="center">
    <h3 align="center">pyx</h3>    
    <p align="center">
        A Python module for creating, reading, and editing Alteryx Designer workflows entirely in code.
        <br />
        <a href="https://github.com/bigangryguy/pyx"><strong>Explore the docs »</strong></a>
        <br />
        <br />
        <a href="https://github.com/bigangryguy/pyx">View Demo</a>
        ·
        <a href="https://github.com/bigangryguy/pyx/issues">Report Bug</a>
        ·
        <a href="https://github.com/bigangryguy/pyx/issues">Request Feature</a>
    </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

A Python module for creating, reading, and editing Alteryx Designer workflows entirely in code.

Using pyx, developers can:
* Read existing Alteryx workflows into a structured set of Python objects
* Create new Alteryx workflows as a structured set of Python objects
* Edit Alteryx workflows and the tools contained within
* Run Alteryx workflows on systems where Alteryx Designer is installed (Windows only)

### Built With

Written and tested using Python 3.8.x. Also uses these Python packages:

* [xmltodict](https://github.com/martinblech/xmltodict)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

You will need to install the following Python modules, either individually or using the included `requirements.txt`:
* xmltodict
```shell script
pip install --user xmltodict
```

Using the `requirements.txt` to install all requirements at once:
```shell script
pip install -r --user requirements.txt
```

### Installation

1. Clone the repo
```sh
git clone https://github.com/bigangryguy/pyx.git
```
2. Install requirements (see above)

There is no installer configured for the module yet, but one is coming soon.

<!-- USAGE EXAMPLES -->
## Usage

The file `example-1.py` shows a complete example of reading and modifying an example workflow (contained in the 
`workflows` folder).

To start, import the `Workflow` and `OutputTool` classes.
```python
from pyx.workflow import Workflow
```

Then read a workflow using the Workflow class static `read()` function.
```python
workflow: Workflow = Workflow.read('workflows/Example-Simple2.yxmd')
```

Next, create a new `OutputTool` instance with a tool ID from the workflow `get_new_tool_id()` helper function. Place the 
new tool below the tool with ID 6 using the workflow `position_below()` helper function.
```python
outputTool: OutputTool = OutputTool(workflow.get_new_tool_id())
outputTool.position = workflow.position_below(6)
```

Many classes use a fluent interface to make chaining function calls possible. Add the new tool to the workflow and 
connect it to the tool with ID 5.
```python
workflow.add_tool(outputTool) \
        .add_connection(5, 'Output', outputTool.tool_id, 'Input')
```

Finally, write the edited workflow to a new file using the Workflow class static `write()` function.
```python
Workflow.write(workflow, 'workflows/Example-1-Output.yxmd')
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/bigangryguy/pyx/issues) for a list of proposed features (and known issues).

* Add more concrete tool implementations
  * Until then, the base Tool class supports all existing tools through the `properties` property, which exposes the 
tool configuration as a set of nested `OrderedDict`. See the `xmltodict` module documentation for the syntax
* Add more API documentation


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.md` for more information.

<!-- CONTACT -->
## Contact

David Wilcox - [@davidtwilcox](https://twitter.com/davidtwilcox) - david@dtwil.co

Project Link: [https://github.com/bigangryguy/pyx](https://github.com/bigangryguy/pyx)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Alteryx](https://www.alteryx.com/)
* [Ned Harding](https://github.com/AlteryxNed/) - Founder and former CTO of Alteryx
