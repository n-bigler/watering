import React, { Component } from "react";
import ReactDOM from "react-dom";
import SwitchContainer from "./SwitchContainer.jsx";

class SwitchGroupContainer extends Component {
	constructor() {
		super();
		this._isMounted = true;
		this.state = {
			switches: [] 
		};
	}

	getSwitches(){
		fetch("http://192.168.1.104:5000/getallnames", {
			method: "GET"
		})
			.then(res => res.json())
			.then(
				(result) => {
					console.log(this._isMounted)
						this.setState({switches: result})
				},
				(error) => {
						this.setState({error})
				}
			);
	}

	componentDidMount() {
		this._isMounted = true;
		this.getSwitches();
	}

	componentWillUnmount() {
		this._isMounted = false;
	}

	render() {
		var switches = []
		for(let it = 0; it < this.state.switches.length; it++){
			console.log(this.state.switches)
			switches.push(
				<SwitchContainer
					id={this.state.switches[it]+"_SwitchContainer"}
					key={this.state.switches[it]+"_SwitchContainer"}
					name={this.state.switches[it]}	
				/>
			);
		}
		return (
			<div id="switchGroup"> 
				{switches}
			</div>
		);
	}
}

export default SwitchGroupContainer;

const wrapper = document.getElementById("switches");
wrapper ? ReactDOM.render(<SwitchGroupContainer />, wrapper) : false;
