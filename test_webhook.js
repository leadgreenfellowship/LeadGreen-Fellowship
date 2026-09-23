fetch('https://lead-green-fellowship-elkd.vercel.app/api/webhook', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'verif-hash': process.argv[2] || 'MySecret123' },
    body: JSON.stringify({
        event: 'charge.completed',
        data: {
            status: 'successful',
            tx_ref: 'test_agent_' + Date.now(),
            amount: 1.99,
            currency: 'USD',
            customer: { name: 'Test AI', email: 'test@leadgreen.org' }
        }
    })
}).then(r => r.text().then(t => console.log('Status:', r.status, 'Body:', t)))
    .catch(e => console.error(e));
