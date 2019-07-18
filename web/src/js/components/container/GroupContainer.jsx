import React, { Component } from "react";
import { Grid } from 'semantic-ui-react';

class GroupContainer extends Component {
	constructor() {
		super();
		this.state = {
			content: []
		}
		this.getContent = this.getContent.bind(this);
	}

	getContent(){
		fetch(this.props.url, {
			method: "GET"
		})
		.then(res => res.json())
		.then(
			(result) => {
				this.setState({content: result});
			},
			(error) => {
					this.setState({error})
			}
		);
	}


	componentDidMount() {
		this._isMounted = true;
		this.getContent();
	}

	componentWillUnmount() {
		this._isMounted = false;
	}

	render() {
		let allContent = [];
		for(let it = 0; it < this.state.content.length; it++){
			let childrenWithProps = React.Children.map(this.props.children, child =>
				React.cloneElement(child, {...this.state.content[it], getContent: this.getContent})  
			);	
			allContent.push(childrenWithProps);
		}
		return (
			<Grid.Row columns={allContent.length>0?allContent.length:1}>
				{allContent}
			</Grid.Row>
		);
	}
}

export default GroupContainer;
