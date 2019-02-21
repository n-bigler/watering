import React, { Component } from "react";
import ReactDOM from "react-dom";
import Logging from "../presentational/Logging.jsx";
import PropTypes from "prop-types";
import autobahn from "autobahn";

function wampMessageToText(message){
	var now = new Date();   
	var nowStr = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
	
	return nowStr + " - " + message.msg;
}


class LoggingContainer extends Component {
	constructor(props) {
		super(props);
		this.state = {
			messages: []
		};
//		this.componentDidMount = this.componentDidMount.bind(this);
	}



	static getDerivedStateFromProps(props, state){
		if(props.message == null || props.message.level==='debug'){
			return null;
		}
		let newTextMessage = wampMessageToText(props.message);
		if(state.messages.length == 0 || newTextMessage !== state.messages[state.messages.length-1]){
			let newMessageList = state.messages;
			newMessageList.push(newTextMessage);
			if(newMessageList.length >= 10){
				newMessageList.shift();
			}
			return newMessageList;
		}
		return null;
	}

// 	onLoggingEvent(args) {
// 		var message = args[0];
// 		console.log("Event:", args);
// 		if(message.level != 'debug'){
// 			var now = new Date();   
// 			var nowStr = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
// 			this.setState(function(state, props) {
// 				var newMsgList = state.messages;
// 				if(newMsgList.length == 10){
// 					newMsgList.shift();
// 				} 
// 				newMsgList.push(nowStr + " - " + message.msg);
// 	
// 				return {
// 					messages: newMsgList 
// 				};
// 			});
// 		}
// 	}
// 	

// 	componentDidMount() {
// 		var connection = new autobahn.Connection({url: "ws://192.168.1.104:8080/ws", realm: "realm1"});
// 
// 		connection.onopen = ((session)  => {
// 			session.subscribe('ch.watering.logging', this.onLoggingEvent);
// 		});
// 		connection.open();
// 	}

	componentWillUnmount(){
	}


	render() {
		return (
			<Logging
				messages={this.state.messages}
			/>
		);
	}
};


export default LoggingContainer;


