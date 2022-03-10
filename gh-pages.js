var ghpages = require('gh-pages');

ghpages.publish(
	'public', // path to public directory
	{
		branch: 'gh-pages',
		user: {
			name: 'Yaseen AlMannaee', // update to use your name
			email: 'commit@yaseen.ae' // Update to use your email
		}
	},
	() => {
		console.log('Deploy Complete!')
	}
)