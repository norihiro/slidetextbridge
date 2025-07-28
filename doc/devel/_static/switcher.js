"use strict";

let current_language = DOCUMENTATION_OPTIONS.LANGUAGE?.toLowerCase() || "en";
let current_root = new URL(document.documentElement.dataset.content_root, window.location).href;
let current_version = (() => {
	let aa = current_root.split("/");
	aa.reverse();
	for (const a of aa) {
		if (a.length)
			return a;
	}
})();
let docs_root = (() => {
	let aa = current_root.split("/");
	if (aa[aa.length-1] == "")
		aa.pop();
	aa.pop();
	if (aa[aa.length-1] == current_language)
		aa.pop();
	return aa.join("/") + "/";
})();
let rel_path = window.location.href.replace(current_root, "");

async function fetch_switcher_data() {
	const res = await fetch(docs_root + "switcher-data.json");
	if (!res.ok)
		throw new Error("Cannot get switcher-data.json");
	return await res.json();
}

async function create_switchers() {
	if (document.querySelector("div.selectors"))
		return;

	const select_lang = document.createElement("select");
	select_lang.className = "selector-language";

	const select_ver = document.createElement("select");
	select_ver.className = "selector-version";

	const selectors = document.createElement("div");
	selectors.className = "selectors";
	selectors.append(select_lang);
	selectors.append(select_ver);

	document.querySelector("h1.logo").insertAdjacentElement("afterend", selectors);

	let data = await fetch_switcher_data();

	for (const lang of data.languages) {
		const option = document.createElement("option");
		option.value = lang.language || "en";
		option.text = lang.display;
		option.selected = option.value == current_language;
		select_lang.append(option);
	}

	for (const v of data.versions) {
		const option = document.createElement("option");
		option.value = v.version;
		option.text = v.display;
		option.selected = option.value == current_version;
		select_ver.append(option);
	}

	select_lang.addEventListener("change", on_language_select);
	select_ver.addEventListener("change", on_version_select);
}

function make_url(language, version) {
	let new_language = language || current_language;
	let new_version = version || current_version;

	if (new_language == "en")
		return docs_root + new_version + "/" + rel_path;
	else
		return docs_root + new_language + "/" + new_version + "/" + rel_path;
}

async function navigate_to_first_existing(urls) {
	for (const url of urls) {
		try {
			let res = await fetch(url, {method: "HEAD"});
			if (res.ok) {
				window.location.href = url;
				return url;
			}
		} catch (err) {
			console.error(`Error to fetch '${url}'; ${err}`);
		}
	}
}

function on_language_select(event) {
	let language = event.target.value;
	if (language == current_language)
		return;

	navigate_to_first_existing([
		make_url(language, current_version),
		make_url(language, "latest"),
	]);
}

function on_version_select(event) {
	let version = event.target.value;
	if (version == current_version)
		return;

	navigate_to_first_existing([
		make_url(current_language, version),
		make_url("en", version),
	]);
}

if (document.readyState !== "loading") {
	create_switchers().catch(console.error);
} else {
	document.addEventListener("DOMContentLoaded", () => {
		create_switchers().catch(console.error);
	});
}
