document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archive').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_email;
  document.querySelector('#back-to-mailbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#back-to-archived').addEventListener('click', () => load_mailbox('archive'))
  document.querySelector('#back-to-sent').addEventListener('click', () => load_mailbox('sent'));


  // By default, load the inbox

  load_mailbox('inbox')

});


function compose_email() {
  clear_all_emails();
  deactivate_current_button('compose');
  activate_disabled_button('inbox');
  activate_disabled_button('sent');
  activate_disabled_button('archive');
  document.querySelector('#compose-recipients').disabled = false;
  document.querySelector('#compose-subject').disabled = false;

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#back-to-mailbox').style.display = 'none';
  document.querySelector('#archive-email').style.display = 'none';
  document.querySelector('#reply-on-email').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function load_mailbox(mailbox) {
  // Update to null view one particular email
  document.querySelector('#view-email').innerHTML = '';

  // List which stores mailbox buttons
  let all_buttons = ['inbox', 'sent', 'archive', 'compose'];
  let filteredButtons = all_buttons.filter(function(e) {return e !== mailbox})
  all_buttons.forEach(box => {
    activate_disabled_button(box);
  });
  deactivate_current_button(mailbox);
  filteredButtons.push(mailbox);
  all_buttons = filteredButtons;

  // Show the emails of particular mailbox
  if (mailbox === 'inbox') {
    get_all_emails(mailbox);
    document.querySelector('#view-email').style.display = 'block';
  } else if (mailbox === 'archive') {
    get_archived_emails(mailbox);
    document.querySelector('#view-email').style.display = 'block';
  } else if (mailbox === 'sent') {
    get_sent_emails(mailbox);
    document.querySelector('#view-email').style.display = 'block';
  } else {
    clear_all_emails();
  }

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#back-to-mailbox').style.display = 'none';
  document.querySelector('#back-to-sent').style.display = 'none';
  document.querySelector('#archive-email').style.display = 'none';
  document.querySelector('#back-to-archived').style.display = 'none';
  document.querySelector('#unarchive-email').style.display = 'none';
  document.querySelector('#reply-on-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

}


function send_email() {
    const recipients = document.querySelector('#compose-recipients').value
    const subject = document.querySelector('#compose-subject').value
    const body = document.querySelector('#compose-body').value

    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
    })
    .then(response => response.json())
        .then(result => {
            if ("message" in result) {
                console.log(result);
                load_mailbox('sent');
                }
            if ("error" in result) {
                console.log(result);
                document.querySelector('#error-occurs').innerHTML = result["error"]
                }
            })
            .catch(error => {
                console.log(error);
        });
    return false;
    }


function get_all_emails(mailbox) {
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        emails.forEach(email => {
            let div = document.createElement('div');
            if (email.read === false) {
                div.style.backgroundColor = 'white';
            } else {
                div.style.backgroundColor = '#CACACA';
            }
            div.style.margin = "20px";
            div.style.padding = "20px";
            div.style.border = "1px solid black"
            div.setAttribute("id", "unique-email");
            div.innerHTML = `FROM: ${email.sender}<br>SUBJECT: ${email.subject}<br>TIMESTAMP: ${email.timestamp}`;
            document.querySelector('#emails-view').append(div);
            div.addEventListener('click', function() {
                view_email(email.id, mailbox, email);
            });
        });
    });
}


function clear_all_emails() {
    document.querySelector('#emails-list').innerHTML = "";
}


function deactivate_current_button(mailbox) {
    document.querySelector(`#${mailbox}`).disabled = true;
}


function activate_disabled_button(mailbox) {
    if (mailbox == 'archive') {
        document.querySelector('#archive').disabled = false;
    } else {
        document.querySelector(`#${mailbox}`).disabled = false;
    }
}


function view_email(email_id, mailbox, email) {
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
                read: true,
                })
            })
        document.querySelector('#emails-view').innerHTML = '';
        document.querySelector('#view-email').innerHTML = `FROM: ${email.sender}<br>SUBJECT: ${email.subject}<br><br>EMAIL:<br>${email.body}`;
        if (mailbox === 'inbox') {
            document.querySelector('#back-to-mailbox').style.display = 'block';
            document.querySelector('#archive-email').style.display = 'block';
            document.querySelector('#reply-on-email').style.display = 'block';
        } else if (mailbox === 'archive') {
            document.querySelector('#back-to-archived').style.display = 'block';
            document.querySelector('#unarchive-email').style.display = 'block';
        } else if (mailbox === 'sent') {
            document.querySelector('#back-to-sent').style.display = 'block';
        }
        document.querySelector('#archive-email').addEventListener('click', () => archive_email(email_id));
        document.querySelector('#unarchive-email').addEventListener('click', () => unarchive_email(email_id));
        document.querySelector('#reply-on-email').addEventListener('click', () => reply_email(email));
    }


function archive_email(email_id) {
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
            })
    })
    load_mailbox('archive');
}


function unarchive_email(email_id) {
    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
            })
    })
    load_mailbox('inbox');
}


function get_archived_emails(mailbox) {
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
            .then(emails => {
                emails.forEach(email => {
                if (email.archived == true) {
                    let div = document.createElement('div');
                    div.setAttribute("id", "arch-email");
                    div.style.margin = "20px";
                    div.style.padding = "20px";
                    div.style.border = "1px solid black"
                    div.innerHTML = `FROM: ${email.sender}<br>SUBJECT: ${email.subject}<br>TIMESTAMP:${email.timestamp}`;
                    document.querySelector('#emails-view').append(div);
                    div.addEventListener('click', function() {
                        view_email(email.id, mailbox, email);
                    });
                }
            })
        })
    }


function get_sent_emails(mailbox) {
    let email_owner = document.querySelector('#owner-of-email').innerHTML
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
            .then(emails => {
                emails.forEach(email => {
                    if (email.sender === email_owner) {
                        let div = document.createElement('div');
                        div.setAttribute('id', 'sent-emails');
                        div.style.margin = "20px";
                        div.style.padding = "20px";
                        div.style.border = "1px solid black"
                        div.innerHTML = `FROM: ${email.sender}<br>SUBJECT: ${email.subject}<br>TIMESTAMP:${email.timestamp}`;
                        document.querySelector('#emails-view').append(div);
                        div.addEventListener('click', function() {
                            view_email(email.id, mailbox, email);
                    });
                }
            })
        })
    }


function reply_email(email) {
    let sender = email.sender;
    let subject = email.subject;
    let timestamp = email.timestamp;
    let text = email.body;
    document.querySelector('#compose-recipients').value = sender;
    document.querySelector('#compose-body').value = `On ${timestamp} ${sender} wrote: ${text}`
    document.querySelector('#compose-subject').value = `Re: ${subject}`;
    document.querySelector('#compose-recipients').disabled = true;
    document.querySelector('#compose-subject').disabled = true;
    document.querySelector('#back-to-mailbox').style.display = 'none';
    document.querySelector('#archive-email').style.display = 'none';
    document.querySelector('#reply-on-email').style.display = 'none';
    document.querySelector('#view-email').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
}