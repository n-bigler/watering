import React, { Component } from "react";
import ReactDOM from "react-dom";
import Switch from "../presentational/Switch.jsx";
import PropTypes from "prop-types";

class SwitchContainer extends Component {
	constructor(props) {
		super(props);
		this._isMounted = false;
		this.state = {
			state: "off"
		};

		this.handleClick = this.handleClick.bind(this);
	}

	getObjState(){
		fetch(`http://192.168.1.104:5000/getstate?name=${this.props.name}`,{
			method: "GET"
		})
			.then(res => res.text())
			.then(
				(result) => {
					if(this._isMounted){
						this.setState({state: result})
					}
				},
				(error) => {
					if(this._isMounted){
						this.setState({error})
					}
				}
			);
	}

	componentDidMount() {
		this._isMounted = true;
		this.getObjState();
	}
	componentWillUnmount(){
		this._isMounted = false;
	}
	handleClick(event) {
		fetch(`http://192.168.1.104:5000/switch?name=${this.props.name}`,{
			method: 'POST'
		})
	  		.then(response => response.text())
			.then(
				(result) => {
				  	if(result == "success"){
						var toSet = "on"
						this.state.state=="on" ? toSet = "off" : toSet = "on"
						this.setState({ state: toSet });
					}
				}
			);
			
	}

	render() {
		return (
			<Switch
				text={this.props.name}
				id={this.props.name + "_Switch"}
				name={this.props.name}
				value={this.state.state}
				handleClick={this.handleClick}
			/>
		);
	}
}

SwitchContainer.propTypes = {
	name: PropTypes.string.isRequired,
	id: PropTypes.string.isRequired
};

export default SwitchContainer;

const wrapper = document.getElementById("switches");
wrapper ? ReactDOM.render(<SwitchContainer />, wrapper) : false;
