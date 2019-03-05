import React, { Component } from "react";
import {Button, Grid, Form, Icon, Input, Select, Card} from "semantic-ui-react";
import AddTimerForm from '../presentational/AddTimerForm.jsx';

class AddTimerContainer extends Component {
	constructor(props) {
		super(props);
		this.state = {
			opened: false,
			time: "",
			process: "",
			allProcesses: []
		}
		this.open = this.open.bind(this);
		this.cancel = this.cancel.bind(this);
		this.submit = this.submit.bind(this);
		this.timeChanged = this.timeChanged.bind(this);
		this.processSelected = this.processSelected.bind(this);
	}
	
	open(event){
		fetch("http://192.168.1.104:5000/getallprocesses", {
			method: "GET"
		})
		.then(res => res.json())
		.then(
			(result) => {
				let allProcessesName = [];
				for (let it = 0; it<result.length; it++){
					allProcessesName.push(result[it]['name']);
				}
				this.setState(state=>({...state, allProcesses: allProcessesName}))
			},
			(error) => {
				this.setState({error})
			}
		);
		this.setState(state=>({...state, opened: true}));
	}
	cancel(event){
		this.setState(state=>({...state, opened: false}));
	}
	submit(event){
		fetch(`http://192.168.1.104:5000/addtimer?time=${this.state.time}&process=${this.state.process}`, {
			method: 'POST'
		})
		.then(response => response.text())
		.then(
			(result) => {
				console.log(result);
			}
		);
	}

	processSelected(e, { value }){
		const newVal = value;
		console.log(newVal);
		this.setState(state => ({
			...state,
			process: newVal
		}));
	}
		
	timeChanged(e){
		const newVal = e.target.value;
		console.log(newVal);
		this.setState(state => ({
			...state,
			time: newVal
		}));
	}

	render() {
		console.log(this.props);
		let element = {};
		if(!this.state.opened){
			element = (
				<Button icon labelPosition='left' onClick={this.open}>
					<Icon name="plus"/>
					Add timer
				</Button>
			);
		}else{
			let processList = [];
			for (let it=0; it<this.state.allProcesses.length; it++){
				processList.push({value: this.state.allProcesses[it], text: this.state.allProcesses[it]});
			}
			element = (<AddTimerForm 
				cancel={this.cancel} 
				submit={this.submit} 
				timeChanged={this.timeChanged}
				processSelected={this.processSelected}
				allProcesses={processList}
			/>);
		}
			
		return (
			<Grid.Row>
			{element}
			</Grid.Row>
		);
	}
}


export default AddTimerContainer;

