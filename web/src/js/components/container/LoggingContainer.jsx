import React, { Component } from "react";
import ReactDOM from "react-dom";
import Logging from "../presentational/Logging.jsx";
import PropTypes from "prop-types";
import autobahn from "autobahn";

class LoggingContainer extends Component {
	constructor(props) {
		super(props);
		this.state = {
			messages: []
		};
		this.onLoggingEvent = this.onLoggingEvent.bind(this);
//		this.componentDidMount = this.componentDidMount.bind(this);
	}

	onLoggingEvent(args) {
		var message = args[0];
		console.log("Event:", args);
		if(message.level != 'debug'){
			var now = new Date();   
			var nowStr = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
			this.setState(function(state, props) {
				var newMsgList = state.messages;
				if(newMsgList.length == 10){
					newMsgList.shift();
				} 
				newMsgList.push(nowStr + " - " + message.msg);
	
				return {
					messages: newMsgList 
				};
			});
		}
	}
	

	componentDidMount() {
		var connection = new autobahn.Connection({url: "ws://192.168.1.104:8080/ws", realm: "realm1"});

		connection.onopen = ((session)  => {
		   	session.subscribe('ch.watering.logging', this.onLoggingEvent);
		});
		connection.open();
	}

	componentWillUnmount(){
	}


	render() {
		console.log(this.state)
		return (
			<div className="row justify-content-center mt-5">
			<Logging
				messages={this.state.messages}
			/>
			</div>
		);
	}
};


export default LoggingContainer;


