import React, { Component } from "react";
import ReactDOM from "react-dom";
import SwitchContainer from "./SwitchContainer.jsx";
import { Grid } from "semantic-ui-react";

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
				(switchesName) => {
					let promises = [];
					for(let it=0; it<switchesName.length; it++){
						let currName = switchesName[it];
						promises.push(this.getDeviceState(currName));
					}
					Promise.all(promises).then((isOn) => {
						let newSwitches = [];
						for(let it=0; it<isOn.length; it++){
							newSwitches.push({'name': switchesName[it], 
								'isOn': isOn[it]});
						}
						this.setState({switches: newSwitches});
					});
				},
				(error) => {
						this.setState({error})
				}
			);
	}

	getDeviceState(name){
		return fetch(`http://192.168.1.104:5000/getstate?name=${name}`,{
			method: "GET"
		})
			.then(res => res.text())
			.then(
				(result) => {
					return (result==='on'?true:false);
				},
				(error) => {
					return error;
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

	static getDerivedStateFromProps(props, state){
		if(props.message != null && props.message.type === 'switchingDevice'){
			let newState = state;
			let device = state.switches.filter((s) => s.name === props.message.device)[0];
			device.isOn = props.message.isOn === "true"?true:false;
			return newState;
		}
		return null;
	}

	render() {
		var switches = []
		for(let it = 0; it < this.state.switches.length; it++){
			switches.push(
				<SwitchContainer
					id={this.state.switches[it]['name']+"_SwitchContainer"}
					key={this.state.switches[it]['name']+"_SwitchContainer"}
					name={this.state.switches[it]['name']}
					isOn={this.state.switches[it]['isOn']}
				/>
			);
		}
		return (
			<Grid.Row columns={switches.length>0?switches.length:1}> 
				{switches}
			</Grid.Row>
		);
	}
}

export default SwitchGroupContainer;

