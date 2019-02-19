import React, { Component } from "react";
import { Grid } from "semantic-ui-react";
import ProcessContainer from "./ProcessContainer.jsx";

class ProcessesGroupContainer extends Component {
	constructor() {
		super();
		this._isMounted = true;
		this.state = {
			processes: [] 
		};
	}

	getProcesses(){
		fetch("http://192.168.1.104:5000/getallprocesses", {
			method: "GET"
		})
			.then(res => res.json())
			.then(
				(result) => {
					console.log(this._isMounted)
						this.setState({processes: result})
				},
				(error) => {
						this.setState({error})
				}
			);
	}

	componentDidMount() {
		this._isMounted = true;
		this.getProcesses();
	}

	componentWillUnmount() {
		this._isMounted = false;
	}

	render() {
		var processes = []
		for(let it = 0; it < this.state.processes.length; it++){
			console.log(this.state.processes[it]);
			processes.push(
				<ProcessContainer
					id={this.state.processes[it]['id']+"_ProcessesContainer"}
					name={this.state.processes[it]['name']}	
					desc={this.state.processes[it]['description']}
				/>
			);
		}
		return (
			<Grid.Row columns={processes.length>0?processes.length:1}>
				{processes}
			</Grid.Row>
		);
	}
}

export default ProcessesGroupContainer;

