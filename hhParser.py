from parse_hh_data import download, parse

resume_ids = download.resume_ids("1", "1.221", 1, 1)
for id in resume_ids:
    resume = download.resume(id)
    resume = parse.resume(resume)
    print(resume['specialization'])
