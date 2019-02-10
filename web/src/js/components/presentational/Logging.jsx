import React, { Component } from "react";
import PropTypes from "prop-types";

const Logging = ({ messages }) => {
		var msgList = [];
  		console.log("here");
		for (let it = messages.length-1; it >= 0; it--){
			msgList.push(
				<li>{ messages[it] }</li>
			);
		}

		return (
			<div className="col">
				<ul>{msgList}</ul>
			</div>
		);
};
					
Logging.propTypes = {
	messages: PropTypes.array.isRequired
};
export default Logging;
