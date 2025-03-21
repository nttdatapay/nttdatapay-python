function openPay(tokenId, merchId, email, number, rURL) {
    const options = {
        'atomTokenId': tokenId,
        'merchId': merchId,
        'custEmail': email,
        'custMobile': number,
        'returnUrl': rURL
    }
    let atom = new AtomPaynetz(options, 'uat')
}
